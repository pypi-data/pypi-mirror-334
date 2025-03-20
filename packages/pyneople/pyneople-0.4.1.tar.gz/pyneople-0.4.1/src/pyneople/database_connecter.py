"""
데이터베이스와 상호작용하는 모듈입니다.
"""

from .functions import get_request, ServerMaintenanceError, attr_flatten
from .character import CharacterFame, CharacterSearch, Timeline
from multiprocessing import Process, Queue, Value
from pymongo import MongoClient
from typing import Callable
from psycopg2 import sql
from typing import Union
import psycopg2

__all__ = [
    'store_fame_data_to_mongodb',
    'store_character_data_to_mongodb',
    'store_timeline_data_to_mongodb',
    'PostgreSQLConnecter',
    'mongodb_to_postgresql'
]

def store_fame_data_to_mongodb(
        arg_mongo_client_instance : MongoClient,
        arg_database_name : str,
        arg_collection_name : str,
        arg_api_key_list : list[str],
        arg_max_fame : int = 100000,
        arg_min_fame : int = 0):
    """
    최근 90일 이내 접속한 110 레벨 이상 캐릭터 전체를 MongoDB에 저장하는 함수
        Args :
            arg_mongo_client_instance(MongoClient) : 저장하려는 MongoDB의 pymongo MongoClient 객체  
            
            arg_database_name(str) : 저장하려는 MongoDB의 database name  
            
            arg_collection_name(str) : 저장하려는 MongoDB의 collection name  
            
            arg_api_key_list(list[str]) : Neople Open API 에서 발급된 api key를 원소로 가지는 list  
            
            arg_max_fame(int) : 조회 하려는 최대 명성

            arg_min_fame(int) : 조회 하려는 최소 명성  
    """
    def task_get_request(character_fame_instance, args_queue, data_queue, completed_tasks_count, tasks_to_be_completed_count):
        """
        args_queue에서 인자 정보를 get하고 데이터를 Neople Open API 에서 가져와서 data_queue에 저장
        """
        while completed_tasks_count.value != tasks_to_be_completed_count:
            if not args_queue.empty():
                args_dict = args_queue.get()
                try:
                    data = character_fame_instance.get_data(**args_dict)
                    print("task get request", end="\r")
                    data_queue.put(data)
                except ServerMaintenanceError:
                    raise Exception("서버 점검중")
                except:
                    args_queue.put(args_dict)

    def task_store_data(character_search_instance, args_queue, data_queue, mongo_collection, completed_tasks_count, tasks_to_be_completed_count):        
        """
        data_queue에서 data를 get하고 MongoDB에 저장 후 다음 인자 정보를 args_queue에 저장
        """        
        while completed_tasks_count.value != tasks_to_be_completed_count:
            # data queue가 비여있지 않다면
            if not data_queue.empty():
                # data queue에서 data get
                data = data_queue.get()
                # 해당 data MongoDB에 그대로 저장
                mongo_collection.insert_one(data)
                data = data['rows']

                # 데이터가 있다면
                if data:

                    # 다음 인자 정보 반환을 위한 작업
                    character_search_instance.parse_data(data[0])
                    max_fame = character_search_instance.fame
                    character_search_instance.parse_data(data[-1])
                    min_fame = character_search_instance.fame
                    
                    # 데이터 수집 여부 확인 하도록 출력
                    print(f"max = {max_fame}, min = {min_fame}, 직업 = {character_search_instance.job_grow_name}", end="\r")
                    
                    # 모든 캐릭터의 명성이 같다면
                    if max_fame == min_fame:
                        # 최대명성을 1만 내림
                        min_fame = max_fame - 1

                    # 명성이 최소값이 arg_min_fame보다 작거나 같으면
                    if min_fame <= arg_min_fame:
                        # 해당 직업 완료
                        completed_tasks_count.value += 1
                        print(f"완료된 직업 개수 {completed_tasks_count.value}", end="\r")
                        continue       
                    
                    # 인자정보 args queue에 저장
                    args_dict = {
                        'arg_min_fame' : arg_min_fame,
                        'arg_max_fame' : min_fame,
                        'arg_job_id' : character_search_instance.job_id,
                        'arg_job_grow_id' : character_search_instance.job_grow_id,
                        'arg_is_all_job_grow' : True
                    }
                    args_queue.put(args_dict)
                # 데이터가 없다면
                else:
                    # 해당 직업 완료
                    completed_tasks_count.value += 1
                    print(f"완료된 직업 개수 {completed_tasks_count.value}", end="\r")
                    continue                

    
    database = arg_mongo_client_instance[arg_database_name]
    collection = database[arg_collection_name]
    data = get_request(f"https://api.neople.co.kr/df/jobs?apikey={arg_api_key_list[0]}")
    data = data['rows']
    job_id_list = []
    for job in data:
        for job_grow in job['rows']:
            job_id_list.append((job['jobId'], job_grow['jobGrowId']))
    tasks_to_be_completed_count = len(job_id_list)
    data_queue = Queue()
    args_queue = Queue()
    completed_tasks_count = Value("i", 0)          
    processes = []  
    for api_key in arg_api_key_list:
        character_fame_instance = CharacterFame(api_key)
        process = Process(target=task_get_request, args=(character_fame_instance, args_queue, data_queue, completed_tasks_count, tasks_to_be_completed_count))
        processes.append(process)
    character_search_instance = CharacterSearch(arg_api_key_list[0])    
    process = Process(target=task_store_data, args=(character_search_instance, args_queue, data_queue, collection, completed_tasks_count, tasks_to_be_completed_count))
    processes.append(process)
    
    # 프로세스 시작
    for process in processes:
        process.start()
    
    # arg_queue에 인자 정보 투입
    for job_id , job_grow_id in job_id_list:
        max_fame = arg_max_fame
        args_dict = {
            'arg_min_fame' : arg_min_fame,
            'arg_max_fame' : max_fame,
            'arg_job_id' : job_id,
            'arg_job_grow_id' : job_grow_id,
            'arg_is_all_job_grow' : True
        }
        args_queue.put(args_dict)
    
    # 프로세스 모두 종료 대기
    for process in processes:
        process.join()

def store_character_data_to_mongodb(
        arg_mongo_client_instance : MongoClient,
        arg_database_name : str,
        arg_collection_name : str,
        arg_api_key_list : list[str],
        arg_pyneople_character_class_list : list,
        arg_total_id_list : list):
    """
    character data를 MongoDB에 저장하는 함수
        Args :
            arg_mongo_client_instance(MongoClient) : 저장하려는 MongoDB의 pymongo MongoClient 객체   
            
            arg_database_name(str) : 저장하려는 MongoDB의 database name  
            
            arg_collection_name(str) : 저장하려는 MongoDB의 collection name  
            
            arg_api_key_list(list[str]) : Neople Open API 에서 발급된 api key를 원소로 가지는 list  
            
            arg_pyneople_character_class_list(list) : pyneopl.character 객체를 원소로 가지는 list  
            
            arg_total_id_list : "server_id character_id"로 이루어진 total_id  
    """    
    def task_get_request(pyneople_instance_list, args_queue, data_queue, completed_tasks_count, tasks_to_be_completed_count):
        while completed_tasks_count.value != tasks_to_be_completed_count:
            if not args_queue.empty():
                args_dict = args_queue.get()
                try:
                    for pyneople_instance in pyneople_instance_list:
                        data = pyneople_instance.get_data(**args_dict)
                        data['total_id'] = pyneople_instance._total_id
                        data_queue.put(data)
                except ServerMaintenanceError:
                    raise Exception("서버점검중")
                except:
                    data_queue.put({"pyneople_fail" : args_dict})

    def task_store_data(data_queue, mongo_collection, completed_tasks_count, tasks_to_be_completed_count, fail_queue):
        while completed_tasks_count.value != tasks_to_be_completed_count:
            if not data_queue.empty():
                data = data_queue.get()
                completed_tasks_count.value += 1
                print(f"{completed_tasks_count.value}/{tasks_to_be_completed_count}", end="\r")
                if data.get("pyneople_fail"):
                    fail_queue.put(data.get("pyneople_fail"))
                else:
                    mongo_collection.insert_one(data)
    
    mongo_database = arg_mongo_client_instance[arg_database_name]
    collection = mongo_database[arg_collection_name]    
    tasks_to_be_completed_count = len(arg_total_id_list)
    completed_tasks_count = Value("i", 0)
    data_queue = Queue()
    args_queue = Queue()
    fail_queue = Queue()
    process_list = []
    for api_key in arg_api_key_list:
        pyneople_instance_list = []
        for pyneople_character_class in arg_pyneople_character_class_list:
            pyneople_instance_list.append(pyneople_character_class(api_key))
        process = Process(target=task_get_request, args=(pyneople_instance_list, args_queue, data_queue, completed_tasks_count, tasks_to_be_completed_count))
        process_list.append(process)
    process = Process(target=task_store_data, args=(data_queue, collection, completed_tasks_count, tasks_to_be_completed_count, fail_queue))
    process_list.append(process)

    for process in process_list:
        process.start()    

    for total_id in arg_total_id_list:
        server_id, character_id = total_id.split()
        args_queue.put({"arg_server_id" : server_id, "arg_character_id" : character_id})

    for process in process_list:
        process.join()    
    
    fail_args_list = []
    while not fail_queue.empty():
        fail_args_dict = fail_queue.get()
        fail_args_list.append(fail_args_dict)
    
    with open('fail_args.txt','w', encoding='utf-8') as f:
        for fail_args_dict in fail_args_list:
            f.write(f"{fail_args_dict['arg_server_id']} {fail_args_dict['arg_character_id']}\n")        
    
def store_timeline_data_to_mongodb(
        arg_mongo_client_instance : MongoClient,
        arg_database_name : str,
        arg_collection_name : str,
        arg_api_key_list : list[str],
        arg_total_id_list : list,
        arg_end_time: str,
        arg_start_time: str = "2017-09-21 00:00",
        arg_code : Union[int, str] = ""):
    
    """
    timeline data를 MongoDB에 저장하는 함수
        Args :
            arg_mongo_client_instance(MongoClient) : 저장하려는 MongoDB의 pymongo MongoClient 객체  
            
            arg_database_name(str) : 저장하려는 MongoDB의 database name  
            
            arg_collection_name(str) : 저장하려는 MongoDB의 collection name  
            
            arg_api_key_list(list[str]) : Neople Open API 에서 발급된 api key를 원소로 가지는 list  
            
            arg_end_time(str) : 타임라인 데이터 마지막 수집 시간 ex) "2024-05-02 05:30",  
            
            arg_start_time(str) : 타임라인 데이터 첫 수집 시간 ex) "2024-04-25 12:00",              
            
            arg_code(int) : 수집하고 싶은 타임라인 코드 ex)201, 202 참조) https://developers.neople.co.kr/contents/guide/pages/all  
            
            arg_total_id_list : "server_id character_id"로 이루어진 total_id  
    """     
    def task_get_request(pyneople_instance, args_queue, data_queue, completed_tasks_count, tasks_to_be_completed_count):
        while completed_tasks_count.value != tasks_to_be_completed_count:
            if not args_queue.empty():
                args_dict = args_queue.get()
                try:
                    data = pyneople_instance.get_data(**args_dict)
                    data['total_id'] = pyneople_instance._total_id
                    data_queue.put(data)
                except ServerMaintenanceError:
                    raise Exception("서버점검중")
                except :
                    data_queue.put({"pyneople_fail" : args_dict})


    def task_store_data(data_queue, mongo_collection, completed_tasks_count, tasks_to_be_completed_count, fail_queue):
        while completed_tasks_count.value != tasks_to_be_completed_count:
            if not data_queue.empty():
                data = data_queue.get()
                completed_tasks_count.value += 1
                print(f"{completed_tasks_count.value}/{tasks_to_be_completed_count}", end="\r")
                if data.get("pyneople_fail"):
                    fail_queue.put(data.get("pyneople_fail"))
                else:
                    mongo_collection.insert_one(data)
    
    mongo_database = arg_mongo_client_instance[arg_database_name]
    collection = mongo_database[arg_collection_name]    
    tasks_to_be_completed_count = len(arg_total_id_list)
    completed_tasks_count = Value("i", 0)
    data_queue = Queue()
    args_queue = Queue()
    fail_queue = Queue()
    process_list = []
    
    for api_key in arg_api_key_list:
        pyneople_instance = Timeline(api_key)
        process = Process(target=task_get_request, args=(pyneople_instance, args_queue, data_queue, completed_tasks_count, tasks_to_be_completed_count))
        process_list.append(process)
    process = Process(target=task_store_data, args=(data_queue, collection, completed_tasks_count, tasks_to_be_completed_count, fail_queue))
    process_list.append(process)

    for process in process_list:
        process.start()    
    
    for total_id in arg_total_id_list:
        print(total_id)
        server_id, character_id = total_id.split()
        args_queue.put({"arg_server_id" : server_id, 
                        "arg_character_id" : character_id,
                        "arg_end_date" : arg_end_time,
                        "arg_last_end_date" : arg_start_time,
                        "arg_code" : arg_code})
    
    for process in process_list:
        process.join()
    
    fail_args_list = []
    while not fail_queue.empty():
        fail_args_dict = fail_queue.get()
        fail_args_list.append(fail_args_dict)
    
    with open('fail_args.txt','w', encoding='utf-8') as f:
        for fail_args_dict in fail_args_list:
            f.write(f"{fail_args_dict['arg_server_id']} {fail_args_dict['arg_character_id']}\n")        

class PostgreSQLConnecter():
    
    def __init__(self, arg_database_connection_dict : dict):
        """
        생성자 함수로 database connect의 인자로 전달되는 dict를 입력받는다.
            Args:
                arg_database_connection_dict(dict) : psycopg2.connect 함수의 인자로 사용될 dict
        """
        self.connection = psycopg2.connect(**arg_database_connection_dict)

    def execute(self, arg_sql : str):
        '''
        sql문을 실행시키고 commit까지 완료 시키는 함수
            Args:
                arg_sql(str) : 실행되어야 하는 sql문
        '''
        
        with self.connection.cursor() as cursor:
            cursor.execute(arg_sql)
            self.connection.commit()


    def fetch(self, arg_query : str):
        '''
        query문을 실행시켜 나오는 결과를 반환한다.
            Args:
                arg_query(str) : 실행되어야 하는 query문
        '''

        with self.connection.cursor() as cursor:
            cursor.execute(arg_query)
            return cursor.fetchall()

    def create_table_query(self, arg_pyneople_instance, arg_data_types : list, arg_constraint_options : str = None):
        """
        PostgreSQLConnecter.create_table 메소드의 arg_columns 매개변수로 사용될 값을 반환하는 함수
            Args:
                arg_pyneople_instance : pyneople instance 혹은 pyneople instance를 원소로 가지는 list  
                
                arg_data_type(list) : VARCHAR(32) PRIMARY KEY 같은 제약 조건을 담은 list  
                
                arg_constraint_options(str) : 해당 테이블의 제약조건 ex) "PRIMARY KEY(characterid, server)"  
        """
        colnames = []
        if isinstance(arg_pyneople_instance ,list):
            for pyneople_instance in arg_pyneople_instance:
                colnames += attr_flatten(pyneople_instance)
        else:
            colnames = attr_flatten(arg_pyneople_instance)
        query = []
        for colname, datatype in list(zip(colnames, arg_data_types)):
            query.append(colname + " " + datatype)
        query = list(map(lambda x : x.replace(".", "_"), query))      
        if arg_constraint_options:
            query =  query + [arg_constraint_options]        
        return query        

    def create_table(self, arg_table_name : str, arg_columns : list[str], arg_drop : bool = False):
        """
        table을 만드는 함수
            Args:
                arg_table_name(str) : 생성하려는 table name
                
                arg_columns(list) : CREATE TABLE {table_name} (); 안에들어가는 문자열 list ex ["characterId VARCHAR(32) PRIMARY KEY", "serverId VARCHAR(32) NOT NULL"]
                
                arg_drop(bool) : {False : 이미 동일한 이름의 table이 있으면 에러발생(default), True : 이미 동일한 이름의 table이 있으면 삭제하고 만든다}
        """    
        columns_str = ', '.join(arg_columns)
        if arg_drop :
            self.execute(f"DROP TABLE IF EXISTS {arg_table_name};")
            self.execute(f"CREATE TABLE {arg_table_name} ({columns_str});")
        else :
            self.execute(f"CREATE TABLE {arg_table_name} ({columns_str});")


    def get_column_names(self, arg_table_name : str):
        """
        해당 table의 column 들의 이름을 list로 반환하는 함수
            Args:
                arg_table_name(str) : 확인하려는 table 이름
        """
        with self.connection.cursor() as cursor:
            cursor.execute(f"Select * FROM {arg_table_name} LIMIT 0")
            column_names = [desc[0] for desc in cursor.description]
            return column_names    


    def get_table_name_list(self):
        '''
        해당 데이터베이스의 table 이름의 list를 반환하는 함수
        '''
        data = self.fetch( 
        """
        SELECT
            table_schema || '.' || table_name
        FROM
            information_schema.tables
        WHERE
            table_type = 'BASE TABLE'
        AND
            table_schema NOT IN ('pg_catalog', 'information_schema');
        """
        )            
        table_name_list = [table_name[0].split(".")[1] for table_name in data]
        return table_name_list


    def insert_into_table(self, arg_cursor , arg_table_name : str, arg_columns : list, arg_data : list, arg_ignore_duplication : bool = True):
        """
        table에 데이터를 삽입하는 함수, 주의사항 : 해당 함수는 connectiom.commit() 을 실행하지 않음
            Args:
                arg_cursor(cursor) : psycopg2 cursor 객체  
                
                arg_table_name(str) : 데이터를 삽입하려는 table name  
                
                arg_columns(list) : 데이터를 삽입하려는 column들의 list ex) ["characterId", "serverId", "jobName"]  
                
                arg_data(list) : [('f2baddf4a296490a4d463cb512a83789', 'anton', '총검사')] <- data 1개여도 이런식으로 삽입  
                
                arg_ignore_duplication(bool) : {True : 중복되는게 있으면 해당 항목만 넘어가고 계속 저장해라, False : 중복되는게 있으면 에러를 발생시켜라}  
        """
        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES {}").format(
            sql.Identifier(arg_table_name),
            sql.SQL(', ').join(map(sql.Identifier, arg_columns)),
            sql.SQL(', ').join(map(sql.Literal, arg_data))
            )
        if arg_ignore_duplication:
            insert_query += sql.SQL(" ON CONFLICT DO NOTHING") 
        arg_cursor.execute(insert_query)                    

def mongodb_to_postgresql(arg_postgresql_connecter : PostgreSQLConnecter, 
                          arg_postgresql_table_name : str,
                          arg_mongo_client : MongoClient, 
                          arg_mongo_database_name : str,
                          arg_mongo_collection_name : str,
                          arg_preprocess_function : Callable, 
                          arg_batch_size : int = 100):
    """
    MomgoDB collection 에 저장된 데이터를 Postgresql로 전처리 후 batch_size씩 저장하는 함수
        Args :
            arg_postgresql_connecter(PostgreSQLConnecter) : pyneople database connecter  
            
            arg_postgresql_table_name(str) :  저장하려는 PostgreSQL table name  
            
            arg_mongo_client(MongoClient) : pymongo 의 MongoClient 객체  
            
            arg_mongo_database_name(str) : MongoDB의 database name  
            
            arg_mongo_collection_name(str) : MongoDB의 collection name  
            
            arg_preprocess_function(Callable) : 전처리 함수(input으로 MongoDB의 document가 들어가며 tuple 또는 tuple로 이루어진 list를 반환해야 한다.)  
            
            arg_batch_size(int) : 한번에 조회, 저장하는 document 개수  
    """
    postgresql_columns = arg_postgresql_connecter.get_column_names(arg_postgresql_table_name)
    postgresql_cursor = arg_postgresql_connecter.connection.cursor()

    mongo_database = arg_mongo_client[arg_mongo_database_name]
    mongo_collection = mongo_database[arg_mongo_collection_name]
    
    total_data_count = mongo_collection.count_documents({})
    count = 0
    
    # MongoDB 데이터 조회 및 PostgreSQL에 삽입
    for skip in range(0, total_data_count, arg_batch_size):

        mongo_cursor = mongo_collection.find().skip(skip).limit(arg_batch_size)
        batch_data = list(mongo_cursor)

        if not batch_data:
            break

        insert_data_list = []
        for document in batch_data:
            if isinstance(arg_preprocess_function(document), tuple):
                insert_data_list.append(arg_preprocess_function(document))
            elif isinstance(arg_preprocess_function(document), list):
                insert_data_list += arg_preprocess_function(document)
            else:
                raise TypeError("전처리 함수는 tuple 또는 list of tuple을 반환해야 합니다.")
        arg_postgresql_connecter.insert_into_table(postgresql_cursor, arg_postgresql_table_name, postgresql_columns, insert_data_list)
        arg_postgresql_connecter.connection.commit()
        count += arg_batch_size
        print(f"{count}/{total_data_count}", end="\r")

    # 연결 종료
    arg_mongo_client.close()
    postgresql_cursor.close()
    print("done")    