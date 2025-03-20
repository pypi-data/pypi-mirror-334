"""
Neople Open API 에서 Character를 기반으로 한 정보를 다루는 모듈입니다.
"""
import asyncio
import datetime
import urllib.parse
from typing import Union
from .functions import get_request, async_get_request, explain_enchant, NeopleOpenAPIError
from .METADATA import SERVER_NAME_2_ID, CHARACTER_SEARCH_NAME, \
                    CHARACTER_INFORMATION_NAME, STATUS_NAME, EQUIPMENT_LIST, AVATAR_LIST, PLATINUM_AVATAR_LIST, \
                    BASE_EQUIPMENT_NAME, EQUIPMENT_NAME, WEAPON_NAME, AVATAR_NAME, PLATINUM_AVATAR_NAME, GROWINFO_NAME, SERVER_ID_2_TOTAL_ID

__all__ = [
    "CharacterSearch",
    "CharacterInformation",
    "Timeline",
    "Status",
    "Equipments",
    "Avatars",
    "Creature",
    "Flag",
    "Talismans",
    "EquipmentTrait",
    "SkillStyle",
    "Buff",
    "CharacterFame"
]

class PyNeople():
    """
    부모 Class로 사용
    """
    def __init__(self, arg_api_key : str):
        """
        클래스 생성 시 Neople Open API key를 입력받는다  
            Args :  
                arg_api_key(str) : Neople Open API key  
        """        
        self._api_key = arg_api_key

class PyNeopleAttributeSetter(PyNeople):
    """
    하위 Attribute를 설정 할 수 있는 PyNeople Class 의 부모 Class
    """
    default_sub_attribute_list = []
    
    @classmethod
    def set_sub_attributes(cls, arg_new_attribute_list : list[str]):
        for new_attribute_name in arg_new_attribute_list:
            if not new_attribute_name in cls.default_sub_attribute_list:
                raise ValueError("사용할 수 없는 attribute 입니다.")
        cls.sub_attribute_list = arg_new_attribute_list

    @classmethod
    def delete_sub_attributes(cls, arg_delete_attribute_list : list[str]):
        for new_attribute_name in arg_delete_attribute_list:
            if not new_attribute_name in cls.default_sub_attribute_list:
                raise ValueError("제거 할 수 없는 attribute 입니다.")
        cls.sub_attribute_list = [sub_attr for sub_attr in cls.default_sub_attribute_list if sub_attr not in arg_delete_attribute_list]

    @classmethod        
    def init_sub_attributes(cls):
        cls.sub_attribute_list = cls.default_sub_attribute_list

class PyneopleCharacter(PyNeopleAttributeSetter):
    
    def get_data(self, arg_server_id : str, arg_character_id : str):
        url = self.get_url(arg_server_id, arg_character_id)
        data = asyncio.run(async_get_request(url))
        # data = get_request(url)
        print("처리")
        data['total_id'] = f"{SERVER_ID_2_TOTAL_ID[arg_server_id]}{arg_character_id}"
        return data
    
    def parse_data(self, arg_data : dict):
        self.total_id = arg_data.get('total_id')
                
class CharacterSearch(PyNeopleAttributeSetter):
    """
    Neople Open API 02. 캐릭터 검색
    """
    default_sub_attribute_list = CHARACTER_SEARCH_NAME.keys()
    sub_attribute_list = default_sub_attribute_list

    def get_url(self, arg_server_name : str, arg_character_name : str):
        if arg_server_name in SERVER_NAME_2_ID.keys():
            arg_server_name = SERVER_NAME_2_ID[arg_server_name]
        elif arg_server_name in SERVER_NAME_2_ID.values():
            pass
        else:
            raise ValueError("서버 이름을 확인하시오")
        self._server_id = arg_server_name
        return f"https://api.neople.co.kr/df/servers/{arg_server_name}/characters?characterName={urllib.parse.quote(arg_character_name)}&limit=1&apikey={self._api_key}"
    
    def get_data(self, arg_server_name : str, arg_character_name : str):
        """
        서버 이름과 캐릭터 이름을 검색하면 기본 정보를 반환
            Args : 
                arg_server_name(str) : 서버 이름  ex) 디레지에, cain  
                
                arg_character_name(str) : 캐릭터 이름 ex) 홍길동
        """
        url = self.get_url(arg_server_name, arg_character_name)
        # parse_data에 매개변수로 사용 될 것을 생각해서 dict를 받을 수 있도록 정보 다듬어서 제공
        try:
            # data = asyncio.run(async_get_request(url)).get("rows")
            data = get_request(url).get("rows")
            if data:
                return data[0]
            else:
                raise NeopleOpenAPIError("{'status': 404, 'code': 'DNF001', 'message': 'NOT_FOUND_CHARACTER'}")
        except IndexError:
            return dict()

    def parse_data(self, arg_data : dict):
        """
        데이터를 정리해서 하위 속성에 저장
            Args :
                arg_data(dict) : Neople Open API 를 통해 받은 data  
                
                attribute_list(iterable of str) : 원하는 하위 속성 명
        """
        # 하위 속성에 데이터 할당
        for attribute_name in CharacterSearch.sub_attribute_list:            
            setattr(self, attribute_name, arg_data.get(CHARACTER_SEARCH_NAME[attribute_name]))


class CharacterInformation(PyneopleCharacter):
    """
    Neople Open API 03. 캐릭터 '기본정보' 조회
    """
    default_sub_attribute_list = CHARACTER_INFORMATION_NAME.keys()
    sub_attribute_list = default_sub_attribute_list

    def get_url(self, arg_server_id : str, arg_character_id : str):
        return f"https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}?apikey={self._api_key}"

    # def get_data(self, arg_server_id : str, arg_character_id : str):
    #     """
    #     영문 서버 이름과 캐릭터 ID 를 검색하면 기본 정보를 반환
    #         Args : 
    #             arg_server_id(str) : 영문 서버 이름  ex) cain  
                
    #             arg_character_name(str) : 캐릭터 ID ex) d018e5f7e7519e34b8ef21db0c40fd98
    #     """    
    #     # self._total_id = f"{arg_server_id} {arg_character_id}"
        
    #     url = self.get_url(arg_server_id, arg_character_id)
    #     data = get_request(url)
    #     data['total_id'] = f"{arg_server_id}{arg_character_id}"
    #     return data

    def parse_data(self, arg_data : dict):
        super().parse_data()
        """
        데이터를 정리해서 하위 속성에 저장
            Args :
                arg_data(dict) : Neople Open API 를 통해 받은 data  
                
                attribute_list(iterable of str) : 원하는 하위 속성 명  
        """
        # 하위 속성에 데이터 할당
        for attribute_name in CharacterInformation.sub_attribute_list:
            setattr(self, attribute_name, arg_data.get(CHARACTER_INFORMATION_NAME[attribute_name]))


class Timeline(PyNeople):
    """
    Neople Open API 04. 캐릭터 '타임라인 정보' 조회
    """
    def get_data(self,  
                 arg_server_id : str, 
                 arg_character_id : str, 
                 arg_end_date : str, 
                 arg_last_end_date : str = "2017-09-21 00:00", 
                 arg_last_end_data : Union[dict, None] = None, 
                 arg_limit : int = 100, 
                 arg_code : Union[int, str] = "",
                 arg_print_log : bool = False):
        """
        서버ID와 캐릭터ID 원하는 수집시간(arg_end_date)을 입력받으면 타임라인데이터를 반환한다.
            Args :
                arg_server_id(str) : 서버ID ex) cain  
                
                arg_character_id(str) : 캐릭터ID ex) d018e5f7e7519e34b8ef21db0c40fd98
                
                arg_end_date(str) : 이 시간까지 수집을 한다 ex) 2023-03-03 15:57  
                
                arg_last_end_date(str) : 이 시간부터 수집을 한다 ex) 2018-03-03 15:57  
                
                arg_last_end_data(dict) : 지금까지 수집한 해당 캐릭터의 마지막 타임라인 데이터  
                
                arg_limit(int) : 한번 request할 때 수집 할 타임라인 데이터의 개수  
                
                arg_code(int) : 수집하고 싶은 타임라인 코드 ex)201, 202 참조) https://developers.neople.co.kr/contents/guide/pages/all  
                
                arg_print_log(boolean) : 데이터 수집의 과정의 print 여부  
        """
        self._total_id = f"{arg_server_id} {arg_character_id}"
        timeline = []
        
        end_date = datetime.datetime.strptime(arg_end_date, '%Y-%m-%d %H:%M')
        start_date = end_date - datetime.timedelta(days=90)
        if start_date < datetime.datetime.strptime(arg_last_end_date, '%Y-%m-%d %H:%M'):
            start_date = datetime.datetime.strptime(arg_last_end_date, '%Y-%m-%d %H:%M')
        next = ""
        while start_date < end_date:
            stop = False
            url = f"""https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/timeline?limit={arg_limit}&code={arg_code}&startDate={start_date.strftime('%Y-%m-%d %H:%M')}&endDate={end_date.strftime('%Y-%m-%d %H:%M')}&next={next}&apikey={self._api_key}"""
            if arg_print_log:
                print(f"서버 = {arg_server_id}, 캐릭터 = {arg_character_id} 시작 = {start_date.strftime('%Y-%m-%d %H:%M')}, 끝 = {end_date.strftime('%Y-%m-%d %H:%M')}")
            data = asyncio.run(async_get_request(url))
            # data = get_request(url)
            next = data['timeline']['next']

            # 데이터가 있다면
            if data['timeline']['rows']:                 
                for log in data['timeline']['rows']:
                    if log == arg_last_end_data:
                        stop = True
                        break
                    else:
                        timeline.append(log)
                # 마지막으로 수집된 타임라인 데이터와 일치하는 항목이 있다면
                if stop:
                    break        

            # 타임라인데이터가 있고 마지막 로그가 캐릭터 생성이라면
            if timeline and timeline[-1]['code'] == 101:
                print("캐릭터 생성 로그를 확인했습니다")
                break

            # 해당기간에 next 데이터가 있으면
            if next:
                continue
            # 해당기간에 next 없으면
            else:
                end_date = start_date
                start_date = end_date - datetime.timedelta(days=90)
                if start_date < datetime.datetime.strptime(arg_last_end_date, '%Y-%m-%d %H:%M'):
                    start_date = datetime.datetime.strptime(arg_last_end_date, '%Y-%m-%d %H:%M')
                next = ""    
                continue
        return {'timeline' : timeline} 

class Status(PyneopleCharacter):
    """
    Neople Open API 05. 캐릭터 '능력치 정보' 조회  
    """    
    default_sub_attribute_list = STATUS_NAME.keys()
    sub_attribute_list = default_sub_attribute_list    

    def get_url(self, arg_server_id : str, arg_character_id : str):
        """
        캐릭터의 모험단명부터 명성 등 정보를 반환한다
            Args:
                arg_server_id(str) :  서버 ID  
                
                arg_character_id(str) : 캐릭터 ID  
        """
        return f'https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/status?apikey={self._api_key}' 

    # def get_data(self, arg_server_id : str, arg_character_id : str):
    #     """
    #     캐릭터의 모험단명부터 명성 등 정보를 반환한다
    #         Args:
    #             arg_server_id(str) :  서버 ID  
                
    #             arg_character_id(str) : 캐릭터 ID  
    #     """
    #     self._total_id = f"{arg_server_id} {arg_character_id}"
    #     url = f'https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/status?apikey={self._api_key}'
    #     return get_request(url)

    def parse_data(self, arg_data : dict):
        """
        데이터를 정리해서 하위 attribute에 저장
            Args :
                arg_data(dict) : Neople Open API 를 통해 받은 data

                attribute_list(iterable of str) : 원하는 하위 속성 명
        """
        
        # 모험단, 길드 버프 정리
        if arg_data.get('buff'):
            for buff in arg_data['buff']:
                if buff.get('name') == '모험단 버프':
                    arg_data['adventure_level'] = buff.get('level')
                elif buff.get('name') == '무제한 길드능력치':
                    arg_data['unlimited_guild_abilities'] = True
                elif buff.get('name') == '기간제 길드능력치':
                    arg_data['limited_guild_abilities'] = True
                else:
                    pass
        
        # 상세 스탯 정리
        if arg_data.get('status'):
            for item in arg_data['status']:
                arg_data[item['name']] = item['value']   
        
        # 하위 속성에 데이터 할당
        for attribute_name in Status.sub_attribute_list:
            setattr(self, attribute_name, arg_data.get(STATUS_NAME[attribute_name])) 

class GrowInfo(PyNeopleAttributeSetter):
    """
    Equipments를 위해 사용되는 Class
    """
    default_sub_attribute_list = GROWINFO_NAME.keys()
    sub_attribute_list = default_sub_attribute_list    
    
    def __init__(self):
        for sub_attribute_name in GrowInfo.sub_attribute_list:
            if sub_attribute_name == "option":
                setattr(self, "transfer", None)
                for i in range(1,5):
                    setattr(self, f"{sub_attribute_name}_{i}", None)
            else:
                setattr(self, sub_attribute_name, None)

    def get_grow_info_data(self, arg_grow_info_dict : dict):
        for sub_attribute_name in GrowInfo.sub_attribute_list:
            if sub_attribute_name == "option":
                if arg_grow_info_dict.get(GROWINFO_NAME[sub_attribute_name]):
                    for i, option in enumerate(arg_grow_info_dict.get(GROWINFO_NAME[sub_attribute_name])):
                        setattr(self, f'option_{i+1}', option.get('explain'))                            
                        if option.get('transfer'):
                            setattr(self, 'transfer', i+1)
            else:   
                setattr(self, sub_attribute_name, arg_grow_info_dict.get(GROWINFO_NAME[sub_attribute_name])) 

class BaseEquipment(PyNeopleAttributeSetter):
    """
    Equipments를 위해 사용되는 Class  
    가장 기초적인 장비 정보를 담으며 다른 장비에 부모클래스로 이용된다.
    """    
    default_sub_attribute_list = BASE_EQUIPMENT_NAME.keys()
    sub_attribute_list = default_sub_attribute_list
    
    def __init__(self):
        for sub_attribute in BaseEquipment.sub_attribute_list:
            setattr(self, sub_attribute, None)

    def get_equipment_data(self, arg_equipment_dict : dict):
        
        for sub_attribute in BaseEquipment.sub_attribute_list:
            if sub_attribute == 'enchant':
                setattr(self, sub_attribute, explain_enchant(arg_equipment_dict.get('enchant')))
            else:    
                setattr(self, sub_attribute, arg_equipment_dict.get(BASE_EQUIPMENT_NAME[sub_attribute]))

class Equipment(BaseEquipment):
    """
    Equipments를 위해 사용되는 Class  
    """ 
    default_sub_attribute_list = EQUIPMENT_NAME.keys()
    sub_attribute_list = default_sub_attribute_list
    def __init__(self):
        super().__init__()
        for sub_attribute in Equipment.sub_attribute_list:
            if sub_attribute == 'grow_info':
                setattr(self, sub_attribute, GrowInfo())
            else:
                setattr(self, sub_attribute, None)

    def get_equipment_data(self, arg_equipment_dict):
        super().get_equipment_data(arg_equipment_dict)
        
        for sub_attribute in Equipment.sub_attribute_list:
            if sub_attribute == 'upgrade_info':
                setattr(self, sub_attribute, arg_equipment_dict.get("upgradeInfo", dict()).get('itemName'))
            elif sub_attribute == 'mist_gear':
                if arg_equipment_dict.get('mistGear'):
                    setattr(self, sub_attribute, 'mist_gear')    
                elif arg_equipment_dict.get('pureMistGear'):
                    setattr(self, sub_attribute, 'pure_mist_gear')
                elif arg_equipment_dict.get('refinedMistGear'):
                    setattr(self, sub_attribute, 'refined_mistgear')
                else :
                    pass                
            elif sub_attribute == 'grow_info':
                if arg_equipment_dict.get("customOption"):
                    getattr(self, sub_attribute).get_grow_info_data(arg_equipment_dict.get('customOption'))
                elif arg_equipment_dict.get("fixedOption"):
                    getattr(self, sub_attribute).get_grow_info_data(arg_equipment_dict.get("fixedOption"))
                else :
                    pass
            else:
                pass    
    

class BakalInfo():
    """
    Equipments를 위해 사용되는 Class
    """

    def __init__(self):
        self.option_1 = None
        self.option_2 = None
        self.option_3 = None

    def get_info_data(self, arg_bakal_info_dict):
        if arg_bakal_info_dict.get('options'):
            for i, option in enumerate(arg_bakal_info_dict.get('options')):
                setattr(self, f'option_{i+1}',option.get('explain'))                

class Asrahan_Info():
    """
    Equipments를 위해 사용되는 Class
    """
    def __init__(self):
        self.memory_cluster = None
        self.memory_destination = None

    def get_info_data(self, arg_asrahan_info_dict):
        for asrahan_info in arg_asrahan_info_dict.get('options', list()):
            if asrahan_info.get('name') == '기억의 종착지':
                self.memory_destination = asrahan_info.get('step')
            else:
                self.memory_cluster = asrahan_info.get('step')

class Weapon(Equipment):
    """
    Equipments를 위해 사용되는 Class
    """
    default_sub_attribute_list = WEAPON_NAME.keys()
    sub_attribute_list = default_sub_attribute_list
    def __init__(self):
        super().__init__()
        for sub_attribute in Weapon.sub_attribute_list:
            if sub_attribute == 'bakal_info':
                self.bakal_info = BakalInfo()
            elif sub_attribute == 'asrahan_info':
                self.asrahan_info = Asrahan_Info()
            else:
                pass    

    def get_equipment_data(self, arg_equipment_dict):
        super().get_equipment_data(arg_equipment_dict)
        for sub_attribute in Weapon.sub_attribute_list:
            getattr(self, sub_attribute).get_info_data(arg_equipment_dict.get(WEAPON_NAME[sub_attribute], dict()))
            
class Equipments(PyneopleCharacter):
    """
    Neople Open API 06. 캐릭터 '장착 장비' 조회
    """    
    default_sub_attribute_list = EQUIPMENT_LIST
    sub_attribute_list = default_sub_attribute_list

    def get_url(self, arg_server_id : str, arg_character_id : str):
        url = f'https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/equip/equipment?apikey={self._api_key}'
        return url

    # def get_data(self, arg_server_id : str, arg_character_id : str):
    #     """
    #     영문 서버 이름과 캐릭터 ID 를 검색하면 장착 장비 정보를 반환
    #         Args : 
    #             arg_server_id(str) : 영문 서버 이름  ex) cain  
                
    #             arg_character_name(str) : 캐릭터 ID ex) d018e5f7e7519e34b8ef21db0c40fd98
    #     """        
    #     self._total_id = f"{arg_server_id} {arg_character_id}"
    #     url = f'https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/equip/equipment?apikey={self._api_key}'
    #     return get_request(url)
    
    def parse_data(self, arg_data : dict):
        """
        데이터를 정리해서 하위 attribute에 저장
            Args :
                arg_data(dict) : Neople Open API 를 통해 받은 data
        """
        # 하위 속성 생성
        self.total_id = arg_data.get("total_id")
        for equipment in Equipments.sub_attribute_list:
            if equipment == 'weapon':
                setattr(self, equipment, Weapon())
            elif equipment == 'title':
                setattr(self, equipment, BaseEquipment())
            elif equipment == 'set_item_info':
                setattr(self, equipment, None)
            elif equipment == 'total_id':
                setattr(self, equipment, None)
            else:
                setattr(self, equipment, Equipment())
                
        # 장착 장비 정보 할당        
        for equipment in arg_data.get('equipment', list()):
            if equipment['slotId'].lower() in Equipments.sub_attribute_list:
                getattr(self, equipment['slotId'].lower()).get_equipment_data(equipment)
            # setattr(self, equipment['slotId'].lower(), equipment_data)
            elif equipment == "set_item_info":
                # 세트 아이템 정보 할당
                if arg_data.get('setItemInfo'):
                    set_item_info_list = []
                    for set_item_info in arg_data.get('setItemInfo'):
                        set_item_name_list = set_item_info.get('setItemName').split()
                        set_item_name_list.insert(-1, f"{set_item_info.get('activeSetNo')}")
                        set_item_info_list.append(" ".join(set_item_name_list))
                    setattr(self, 'set_item_info', ", ".join(set_item_info_list))
                else:
                    pass
            else:
                pass        

class Avatar(PyNeopleAttributeSetter):
    """
    Avatars를 위해 사용되는 Class
    """
    default_sub_attribute_list = AVATAR_NAME.keys()
    sub_attribute_list = default_sub_attribute_list
    
    def __init__(self):
        for sub_attribute in Avatar.sub_attribute_list:
            if sub_attribute == "emblems":
                for i in range(1,3):
                    setattr(self, f"{sub_attribute}_{i}", None)
            else:
                setattr(self, sub_attribute, None)

    def get_avatar_data(self, arg_avatar_dict):
        for sub_attribute in Avatar.sub_attribute_list:
            if sub_attribute == 'emblems':
                for emblem in arg_avatar_dict.get('emblems', dict()):
                    setattr(self, f"{sub_attribute}_{emblem.get('slotNo')}", emblem.get('itemName'))
            else:    
                setattr(self, sub_attribute, arg_avatar_dict.get(AVATAR_NAME[sub_attribute]))




class PlatinumAvatar(Avatar):
    """
    Avatars를 위해 사용되는 Class
    """   
    sub_attribute_list = PLATINUM_AVATAR_NAME.keys()
    def __init__(self):
        for sub_attribute in PlatinumAvatar.sub_attribute_list:
            if sub_attribute == "emblems":
                for i in range(1,3):
                    setattr(self, f"{sub_attribute}_{i}", None)
            elif sub_attribute == "platinum_emblem":
                setattr(self, sub_attribute, None)    
            else:
                setattr(self, sub_attribute, None)

    def get_avatar_data(self, arg_avatar_dict):
        
        for sub_attribute in PlatinumAvatar.sub_attribute_list:
            if sub_attribute == 'emblems':
                for emblem in arg_avatar_dict.get(PLATINUM_AVATAR_NAME[sub_attribute], dict()):
                    if emblem.get('slotColor') != '플래티넘':
                        setattr(self, f"{sub_attribute}_{emblem.get('slotNo') - 1}", emblem.get('itemName'))
            elif sub_attribute == "platinum_emblem":
                for emblem in arg_avatar_dict.get(PLATINUM_AVATAR_NAME[sub_attribute], dict()):
                    if emblem.get('slotColor') == '플래티넘':
                        setattr(self, sub_attribute, emblem.get('itemName'))
            else:    
                setattr(self, sub_attribute, arg_avatar_dict.get(AVATAR_NAME[sub_attribute]))

class Avatars(PyneopleCharacter):
    """
    Neople Open API 07. 캐릭터 '장착 아바타' 조회
    """       
    default_sub_attribute_list = AVATAR_LIST
    sub_attribute_list = default_sub_attribute_list

    def get_url(self, arg_server_id: str, arg_character_id : str):    
        return f'https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/equip/avatar?apikey={self._api_key}' 

    # def get_data(self, arg_server_id: str, arg_character_id : str):    
    #     """
    #     영문 서버 이름과 캐릭터 ID 를 검색하면 장착 아바타 정보를 반환
    #         Args : 
    #             arg_server_id(str) : 영문 서버 이름  ex) cain
                
    #             arg_character_name(str) : 캐릭터 ID ex) d018e5f7e7519e34b8ef21db0c40fd98
    #     """
    #     self._total_id = f"{arg_server_id} {arg_character_id}"
    #     url = f'https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/equip/avatar?apikey={self._api_key}'
    #     return get_request(url)

    def parse_data(self, arg_data : dict):
        """
        데이터를 정리해서 하위 attribute에 저장
            Args :
                arg_data(dict) : Neople Open API 를 통해 받은 data
        """        
        self.total_id = arg_data.get("total_id")
        # 하위 속성 생성
        for avatar in Avatars.sub_attribute_list:
            if avatar in PLATINUM_AVATAR_LIST:
                setattr(self, avatar, PlatinumAvatar())    
            else:
                setattr(self, avatar, Avatar())
        
        # 하위 속성에 데이터 할당
        for avatar in arg_data.get('avatar', list()):
            if avatar["slotId"].lower() in Avatars.sub_attribute_list:
                getattr(self, f'{avatar["slotId"].lower()}').get_avatar_data(avatar)


class Creature(PyneopleCharacter):
    """
    Neople Open API 08. 캐릭터 '장착 크리쳐' 조회
    """
    def get_url(self, arg_server_id : str, arg_character_id : str):
        return f"https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/equip/creature?apikey={self._api_key}"

    # def get_data(self, arg_server_id : str, arg_character_id : str):
    #     """
    #     영문 서버 이름과 캐릭터 ID 를 검색하면 장착 크리쳐 정보를 반환
    #         Args : 
    #             arg_server_id(str) : 영문 서버 이름  ex) cain
                
    #             arg_character_name(str) : 캐릭터 ID ex) d018e5f7e7519e34b8ef21db0c40fd98
    #     """
    #     self._total_id = f"{arg_server_id} {arg_character_id}"
    #     url = f"https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/equip/creature?apikey={self._api_key}"
    #     return get_request(url)
    
    def parse_data(self, arg_data : dict):
        """
        데이터를 정리해서 하위 attribute에 저장
            Args :
                arg_data(dict) : Neople Open API 를 통해 받은 data
        """
        self.total_id = arg_data.get("total_id")
        self.creature = arg_data.get('creature', dict()).get('itemName')
        
class Flag(PyneopleCharacter):
    """
    Neople Open API 09. 캐릭터 '장착 휘장' 조회
    """
    def get_url(self, arg_server_id : str, arg_character_id : str):
        return f"https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/equip/flag?apikey={self._api_key}"

    # def get_data(self, arg_server_id : str, arg_character_id : str):
    #     """
    #     영문 서버 이름과 캐릭터 ID 를 검색하면 장착 휘장 정보를 반환
    #         Args : 
    #             arg_server_id(str) : 영문 서버 이름  ex) cain
                
    #             arg_character_name(str) : 캐릭터 ID ex) d018e5f7e7519e34b8ef21db0c40fd98
    #     """        
    #     self._total_id = f"{arg_server_id} {arg_character_id}"
    #     url = f"https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/equip/flag?apikey={self._api_key}"
    #     return get_request(url)
    
    def parse_data(self, arg_data):
        """
        데이터를 정리해서 하위 attribute에 저장
            Args :
                arg_data(dict) : Neople Open API 를 통해 받은 data
        """        
        self.total_id = arg_data.get("total_id")
        self.gem_1 = None       # 젬1 레어도
        self.gem_2 = None       # 젬2 레어도
        self.gem_3 = None       # 젬3 레어도
        self.gem_4 = None       # 젬4 레어도
        self.item_rarity = arg_data.get('flag', dict()).get('itemRarity')   # 휘장 레어도
        self.reinforce = arg_data.get('flag', dict()).get('reinforce')      # 휘장 강화 수치
        for i, gem in enumerate(arg_data.get('flag', dict()).get('gems', list())):
            setattr(self, f"gem_{i+1}", gem.get("itemRarity"))

class Talisman():
    """
    Talismans를 위해 사용되는 Class 
    """

    def __init__(self):
        self.item_name = None
        self.rune_1 = None
        self.rune_2 = None
        self.rune_3 = None   
    
    def get_talisman_data(self, arg_talisman_data):
        self.item_name = arg_talisman_data.get('talisman', dict()).get('itemName')
        for i, rune in enumerate(arg_talisman_data.get('runes', list())):
            setattr(self, f'rune_{i+1}', rune.get('itemName'))        

class Talismans(PyneopleCharacter):
    """
    Neople Open API 10. 캐릭터 '장착 탈리스만' 조회
    """ 

    def get_url(self, arg_server_id : str, arg_character_id : str):
        return f"https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/equip/talisman?apikey={self._api_key}"

    # def get_data(self, arg_server_id : str, arg_character_id : str):
    #     """
    #     영문 서버 이름과 캐릭터 ID 를 검색하면 장착 탈리스만 정보를 반환
    #         Args : 
    #             arg_server_id(str) : 영문 서버 이름  ex) cain
                
    #             arg_character_name(str) : 캐릭터 ID ex) d018e5f7e7519e34b8ef21db0c40fd98
    #     """                
    #     self._total_id = f"{arg_server_id} {arg_character_id}"
    #     url = f"https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/equip/talisman?apikey={self._api_key}"         
    #     return get_request(url)
    
    def parse_data(self, arg_data : dict):
        """
        데이터를 정리해서 하위 attribute에 저장
            Args :
                arg_data(dict) : Neople Open API 를 통해 받은 data
        """        
        self.total_id = arg_data.get("total_id")
        for i, talisman in enumerate(arg_data.get("talismans", list())):
            setattr(self, f"talisman_{i+1}", Talisman())
            getattr(self, f"talisman_{i+1}").get_talisman_data(talisman)        


class EquipmentTrait(PyneopleCharacter):
    """
    Neople Open API 11. 캐릭터 '장비 특성' 조회
    """ 

    def get_url(self, arg_server_id : str, arg_character_id : str):
        return f"https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/equip/equipment-trait?apikey={self._api_key}" 

    # def get_data(self, arg_server_id : str, arg_character_id : str):
    #     """
    #     영문 서버 이름과 캐릭터 ID 를 검색하면 장비 특성 정보를 반환
    #         Args : 
    #             arg_server_id(str) : 영문 서버 이름  ex) cain
                
    #             arg_character_name(str) : 캐릭터 ID ex) d018e5f7e7519e34b8ef21db0c40fd98
    #     """                
    #     self._total_id = f"{arg_server_id} {arg_character_id}"
    #     url = f"https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/equip/equipment-trait?apikey={self._api_key}"
    #     return get_request(url)
    
    def parse_data(self, arg_data : dict):
        """
        데이터를 정리해서 하위 attribute에 저장 강력한 일격과 명상의 레벨만 확인
            Args :
                arg_data(dict) : Neople Open API 를 통해 받은 data  
        """
        self.total_id = arg_data.get("total_id")
        self.total_point = arg_data.get("equipmentTrait", dict()).get("total", dict()).get("point")
        self.category_name = arg_data.get("equipmentTrait", dict()).get("category", dict()).get("name")
        self.strong_hit_level = 0
        self.meditation_level = 0
        option_list = arg_data.get("equipmentTrait", dict()).get("options", list())
        option_list = list(filter(lambda x : x.get("name") in ["[강력한 일격]", "[명상]"], option_list))
        for option in option_list:
            if option.get("name") == "[강력한 일격]":
                self.strong_hit_level = option.get("level")
            else:
                self.meditation_level = option.get("level")


class SkillStyle(PyneopleCharacter):
    """
    Neople Open API 12. 캐릭터 '스킬 스타일' 조회
    """ 

    def get_url(self, arg_server_id : str, arg_character_id : str):
        return f"https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/skill/style?apikey={self._api_key}" 

    # def get_data(self, arg_server_id : str, arg_character_id : str):
    #     """
    #     영문 서버 이름과 캐릭터 ID 를 검색하면 스킬 스타일 정보를 반환
    #         Args : 
    #             arg_server_id(str) : 영문 서버 이름  ex) cain
                
    #             arg_character_name(str) : 캐릭터 ID ex) d018e5f7e7519e34b8ef21db0c40fd98
    #     """                
    #     self._total_id = f"{arg_server_id} {arg_character_id}"
    #     url = f"https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/skill/style?apikey={self._api_key}"
    #     return get_request(url)

    def parse_data(self, arg_data : dict):
        """
        데이터를 정리해서 하위 attribute에 저장 스킬 코드만 구현 완료 나머지 추후 개발
            Args :
                arg_data(dict) : Neople Open API 를 통해 받은 data  
        """        
        self.total_id = arg_data.get("total_id")
        self.skill_code = arg_data.get("skill", dict()).get("hash")

class BuffAvatar():
    """
    Buff를 위해 사용되는 Class
    """
    def __init__(self):
        self.item_name = None
    def get_buff_avatar_data(self, arg_avatar_dict):
        try: 
            self.item_name = arg_avatar_dict['itemName']
        except:
            pass

class BuffPlatimun(BuffAvatar):
    """
    Buff를 위해 사용되는 Class
    """    
    def __init__(self):
        super().__init__()    
        self.option = None
        self.platinum = None
    
    def get_buff_avatar_data(self, arg_avatar_dict):
        super().get_buff_avatar_data(arg_avatar_dict)
        self.option = arg_avatar_dict.get('optionAbility')
        if arg_avatar_dict.get('emblems'):
            for emblems in arg_avatar_dict.get('emblems'):
                if emblems.get('slotColor') == '플래티넘':
                    self.platinum = emblems.get('itemName')


class Buff(PyNeople):
    """
    Neople Open API 13. 캐릭터 "버프 스킬 강화 장착 장비" 조회
    Neople Open API 14. 캐릭터 "버프 스킬 강화 장착 아바타" 조회
    Neople Open API 15. 캐릭터 "버프 스킬 강화 장착 크리쳐" 조회
    """
         
    def get_data(self, arg_server_id : str, arg_character_id : str):
        """
        영문 서버 이름과 캐릭터 ID 를 검색하면 버프 강화(장비, 아바타, 크리쳐) 정보를 반환
            Args : 
                arg_server_id(str) : 영문 서버 이름  ex) cain
                
                arg_character_name(str) : 캐릭터 ID ex) d018e5f7e7519e34b8ef21db0c40fd98
        """   
        # self._total_id = f"{arg_server_id} {arg_character_id}"
        buff_info_dict = {}     
        
        buff_equipment_data = asyncio.run(async_get_request(f"https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/skill/buff/equip/equipment?apikey={self._api_key}"))
        buff_avatar_data = asyncio.run(async_get_request(f"https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/skill/buff/equip/avatar?apikey={self._api_key}"))
        buff_creature_data = asyncio.run(async_get_request(f"https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/skill/buff/equip/creature?apikey={self._api_key}"))
        # buff_avatar_data = get_request(f"https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/skill/buff/equip/avatar?apikey={self._api_key}")
        # buff_creature_data = get_request(f"https://api.neople.co.kr/df/servers/{arg_server_id}/characters/{arg_character_id}/skill/buff/equip/creature?apikey={self._api_key}")
        buff_info_dict["equipment"] = buff_equipment_data
        buff_info_dict["avatar"] = buff_avatar_data
        buff_info_dict["creature"] = buff_creature_data
        buff_info_dict['total_id'] = f"{SERVER_ID_2_TOTAL_ID[arg_server_id]}{arg_character_id}"
        return buff_info_dict

    def parse_data(self, arg_data : dict):
        """
        데이터를 정리해서 하위 attribute에 저장
            Args :
                arg_data(dict) : Neople Open API 를 통해 받은 data
        """         
        # 하위 속성 생성
        self.total_id = arg_data.get('total_id')
        self.buff_level = None
        self.buff_desc = None
        for equipment in EQUIPMENT_LIST:
            if equipment == 'total_id':
                continue
            else:
                setattr(self, f"equipment_{equipment}", None)
        for avatar in list(set(AVATAR_LIST) - set(PLATINUM_AVATAR_LIST)):
            setattr(self, f"avatar_{avatar}", BuffAvatar())
        for avatar in PLATINUM_AVATAR_LIST:
            # print(avatar)
            setattr(self, f"avatar_{avatar}", BuffPlatimun())
        
        self.buff_creature = None  
        arg_buff_equipment_data = arg_data["equipment"]
        arg_buff_avatar_data = arg_data["avatar"]
        arg_buff_creature_data = arg_data["creature"]

        if arg_buff_equipment_data.get("skill", dict()).get('buff'):
            arg_buff_equipment_data = arg_buff_equipment_data.get("skill", dict()).get('buff')
            # 버프 강화 장비
            if arg_buff_equipment_data.get("equipment"):
                for buff_equipment in arg_buff_equipment_data.get("equipment"):
                    setattr(self, f'equipment_{buff_equipment.get("slotId").lower()}', buff_equipment.get('itemName'))
                    if buff_equipment.get("slotId") == 'TITLE':
                        setattr(self, f'equipment_{buff_equipment.get("slotId").lower()}_enchant', explain_enchant(buff_equipment.get('enchant')))
                    else:
                        pass
            else:
                pass
            # 버프 강화 정보
            if arg_buff_equipment_data.get("skillInfo"):
                for index, value in enumerate(arg_buff_equipment_data['skillInfo']['option']['values']):
                    arg_buff_equipment_data['skillInfo']['option']['desc'] = arg_buff_equipment_data['skillInfo']['option']['desc'].replace("{" + f"value{index + 1}" + "}", value)
                self.buff_level = arg_buff_equipment_data['skillInfo']['option']['level']
                self.buff_desc = arg_buff_equipment_data['skillInfo']['option']['desc']              
            
    
        # 버프 강화 아바타
        if arg_buff_avatar_data.get("skill", dict()).get('buff'):
            arg_buff_avatar_data = arg_buff_avatar_data.get("skill", dict()).get('buff')
            if arg_buff_avatar_data.get("avatar"):
                for buff_avatar in arg_buff_avatar_data.get("avatar"):
                    if buff_avatar.get("slotId").lower() in PLATINUM_AVATAR_LIST:
                        getattr(self, f'avatar_{buff_avatar.get("slotId").lower()}').get_buff_avatar_data(buff_avatar)
                    else:
                        getattr(self, f'avatar_{buff_avatar.get("slotId").lower()}').get_buff_avatar_data(buff_avatar)

        # 버프 강화 크리쳐
        if arg_buff_creature_data.get("skill", dict()).get('buff'):
            arg_buff_creature_data = arg_buff_creature_data.get("skill", dict()).get('buff')
            if arg_buff_creature_data.get('creature'):
                for creature in arg_buff_creature_data.get('creature'):
                    setattr(self, 'creature', creature.get('itemName'))

class CharacterFame(PyNeople):
    """
    Neople Open API 16. 캐릭터 명성 검색
    """    
    def get_data(self, arg_min_fame : int, 
                  arg_max_fame : int,
                  arg_job_id : str = "",
                  arg_job_grow_id : str = "",
                  arg_is_all_job_grow : bool = False, 
                  arg_is_buff : bool = "", 
                  arg_server_id : str = "all",
                  arg_limit : int = 200):
        """
        해당 명성 구간의 캐릭터 정보를 원소로 가지는 list를 반환함
            Args : 
                arg_min_fame(int) : 명성 구간 최소값(최대 명성과의 차이가 2000이상이면 최대명성 - 2000 으로 입력됨)
                
                arg_max_fame(int) : 명성 구간 최대값
                
                arg_job_id(str) : 캐릭터 직업 고유 코드
                
                arg_job_grow_id(str) : 캐릭터 전직 직업 고유 코드(jobId 필요)
                
                arg_is_all_job_grow(bool) : jobGrowId 입력 시 연계되는 전체 전직 포함 조회 ex) 검성 -> 웨펀마스터, 검성, 검신, 眞웨펀마스터
                
                arg_is_buff(bool) : 버퍼만 조회(true), 딜러만 조회(false), 전체 조회(미 입력)	
                
                arg_server_id(str) : 서버 아이디
                
                arg_limit(int) : 반환 Row 수
        """
        url = f"https://api.neople.co.kr/df/servers/{arg_server_id}/characters-fame?minFame={arg_min_fame}&maxFame={arg_max_fame}&jobId={arg_job_id}&jobGrowId={arg_job_grow_id}&isAllJobGrow={arg_is_all_job_grow}&isBuff={arg_is_buff}&limit={arg_limit}&apikey={self._api_key}"
        return asyncio.run(async_get_request(url))
    