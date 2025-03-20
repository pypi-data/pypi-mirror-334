# pyneople
Neople Open API wrapper for data analyst

## Documents
[pyneople](https://pyneople.readthedocs.io/ko/latest/index.html).

### Installation
```bash
pip install pyneople
```

## Simple Usage
```python
from pyneople.character import CharacterSearch
api_key = "Neople Open API 에서 발급받은 API key"
character_search = CharacterSearch(api_key)
data = character_search.get_data("서버이름", "캐릭터이름")
character_search.parse_data(data)

print(character_search.server_id) 
print(character_search.character_name)
```

## Step 0. 시작에 앞서
#### Neople Open API 가입 후 api key 확보하기  
1. [Neople Open API](https://developers.neople.co.kr/) 접속 후 로그인
2. 우측 상단의 마이페이지 클릭
3. 어플리케이션 등록

## Step 1. 캐릭터 데이터 가져오기
pyneople.character 내부의 클래스를 이용해서 데이터를 가져옵니다.
```python
from pyneople.character import CharacterInformation
api_key = "Neople Open API 에서 발급받은 API key"

# api_key를 이용해 객체를 생성합니다
character_info = CharacterInformation(api_key)

# get_data 메서드를 이용해 데이터를 가져옵니다
data = character_info.get_data("cain", "d018e5f7e7519e34b8ef21db0c40fd98")

print(data)
```

## Step 2. 캐릭터 데이터 정리하기
객체의 하위 속성을 생성하도록 데이터를 정리합니다.

원하는 데이터만 하위 속성으로 생성하는 클래스 메서드를 가지는 클래스는 다음과 같습니다.
CharacterSearch, CharacterInformation, Status, GrowInfo, BaseEquipment, Equipment, Weapon, Equipments, Avatar, PlatinumAvatar, Avatars
```python
# parse_data 메서드를 이용해 가져온 데이터를 기반으로 하위 속성을 생성합니다.
character_info.parse_data(data)

# 이제 character_info 객체의 하위 속성이 생성되어 확인할 수 있습니다.
print(character_info.character_name)

# pyneople.functions 내의 attr_flatten 함수를 이용해서 모든 하위 속성의 이름을 리스트로 확인할 수 있습니다.
from pyneople.functions import attr_flatten
print(attr_flatten(character_info))

# pyneople.functions 내의 value_flatten 함수를 이용해서 모든 하위 속성의 값을 리스트로 확인할 수 있습니다.
from pyneople.functions import value_flatten
print(value_flatten(character_info))

# python 내장함수를 이용하면 하위 속성의 이름을 key, 값을 value로 가지는 dictionary를 받을 수 있습니다.
character_info_dict = dict(zip(attr_flatten(character_info), value_flatten(character_info)))
print(character_info_dict)
```

## Step 3. 원하는 데이터만 정리하기
다음과 같은 클래스만 사용할 수 있습니다.
CharacterSearch, CharacterInformation, Status, GrowInfo, BaseEquipment, Equipment, Weapon, Equipments, Avatar, PlatinumAvatar, Avatars

```python
# 클래스 메서드를 이용해서 원하는 데이터만 하위 속성으로 생성할 수 있습니다.
# set_sub_attributes 이후 모든 character_infous class 객체는 parse_data 메서드 사용시 지정한 정보만 하위 속성으로 생성합니다.
CharacterInformation.set_sub_attributes(["character_name", 'level', 'job_grow_name'])
del character_info
character_info = CharacterInformation(api_key)
character_info.parse_data(data)
print(attr_flatten(character_info))

# 하위 속성을 기본값으로 초기화 하려면 init_sub_attributes 클래스 메서드를 사용합니다.
CharacterInformation.init_sub_attributes()
del character_info
character_info = CharacterInformation(api_key)
character_info.parse_data(data)
print(attr_flatten(character_info))
```

## Step 4. MongoDB로 데이터 저장하기
pymongo의 MongoClient객체를 확보 후 진행해야 합니다.
```python
from pyneople.database_connecter import store_fame_data_to_mongodb
from pymongo import MongoClient
mongo_client = MongoClient('mongodb://localhost:27017/')
store_fame_data_to_mongodb(mongo_client, 'dnf', 'fame_tb_20240508', [api_key])
```
해당 함수가 실행되면 로컬 MongoDB의 'dnf'라는 이름을 가지는 데이터베이스에 'fame_tb_20240508'라는 이름을 가지는 collection에 최근 90일간 접속기록이 있는 110레벨 캐릭터 전부를 저장합니다.  
또한 api_key를 여러개 사용할 수 있습니다.  
다만 CPU의 코어 수에 따라 데이터 수집 속도 향상이 이루어 질 수 없는 경우도 생깁니다.  
CPU 코어수 이상의 api key를 사용하는 것을 권장하지 않습니다.

## Step 5. PostgreSQL 조작하기
pyneople.database_connecter에서 PostgreSQL 조작을 할 수 있습니다.
```python
from pyneople.database_connecter import PostgreSQLConnecter
# 생성자 함수의 매개변수로 psycopg2 connect함수의 매개변수로 사용될 dict를 입력합니다
# 해당 dict는 예시입니다. 데이터베이스에 적합하게 수정 후 이용해야 합니다.
pg_dict = {
    'host' : 'localhost', 
    'user' : 'dnfdba', 
    'password':'1234', 
    'database':'dnf'
}
pg_connecter = PostgreSQLConnecter(pg_dict)

# 원하는 쿼리문을 입력하면 실행시켜주는 메서드입니다.
query = \
"""
원하는 쿼리문을 입력합니다.
;"""
pg_connecter.excute(query)

# 원하는 쿼리문(SELCT)을 입력하면 결과를 반환하는 메서드입니다.
query = \
"""
SELECT * 
FROM table_name
LIMIT 10
;"""
data = pg_connecter.fetch(query)
print(data)

# table을 생성하는 메서드입니다.
pg_connecter.create_table("timeline_tb_20240502",
            ["total_id VARCHAR(43)",
             "timeline_code SMALLINT",
             "timeline_date TIMESTAMP",
             "timeline_data TEXT"
             ], 
            arg_drop=True)

# table을 생성하는 메서드에 매개변수로 사용 될 리스트를 반환하는 메서드입니다.
CharacterInformation.set_sub_attributes(["character_name", 'level', 'job_grow_name'])
del character_info
character_info = CharacterInformation(api_key)
data = character_info.get_data("cain", "d018e5f7e7519e34b8ef21db0c40fd98")
character_info.parse_data(data)
pg_connecter.create_table_query(character_info, ['VARCHAR(16)', 'SMALLINT', "VARCHAR(16)"])

# table의 필드 리스트를 반환하는 메서드입니다.
print(pg_connecter.get_column_names("table_name"))

# table 이름의 리스트를 반환하는 메서드입니다.
print(pg_connecter.get_table_name_list())

# table에 데이터를 삽입하는 함수입니다.
pg_connecter.insert_into_table(
    pg.cursor, 
    "table_name",  
    ["character_name", "level", "job_grow_name"], 
    [("쑤남", "110", "스트라이커")]
    )
```

## Step 6. MongoDB에 저장된 데이터를 PostgreSQL로 이동하기
```python
from pyneople.database_connecter import mongodb_to_postgresql
# 전처리 함수를 미리 정의해야 합니다
# 전처리 함수는 반드시 tuple 또는 tuple을 원소로 가지는 list를 반환해야 합니다.
def prepro(document):
    document = document['rows']
    data = []
    for character in document:
        cs.parse_data(character)
        value_flatten(cs)
        data.append(tuple(
            [f"{cs.server_id} {cs.character_id}",
            cs.character_name,
            cs.level,
            cs.job_name,
            cs.job_grow_name,
            cs.fame]
        ))
    return data    
mongodb_to_postgresql(pg_connecter, 'fame_tb_20240501', mongo_client, 'dnf', 'fame_tb_20240502', prepro)
```