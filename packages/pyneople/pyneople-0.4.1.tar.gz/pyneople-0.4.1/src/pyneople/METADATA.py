# 초기 설정값
SETTINGS = {
    "request_time_out" : 5,
    "request_time_sleep" : 0.0015
}

# 서버 NAME 이 key ID 가 value
SERVER_NAME_2_ID = {
    "안톤" : "anton",
    "바칼" : "bakal",
    "카인" : "cain",
    "카시야스" : "casillas",
    "디레지에" : "diregie",
    "힐더" : "hilder",
    "프레이" : "prey",
    "시로코" : "siroco"
    }

# 서버 ID 가 key NAME 이 value
SERVER_ID_2_NAME = {v : k for k , v in SERVER_NAME_2_ID.items()}

# 서버 ID 가 total_id에 저장되는 값
SERVER_ID_2_TOTAL_ID = {
    'anton': 'a',
    'bakal': 'b',
    'cain': 'c',
    'casillas': 'k',
    'diregie': 'd',
    'hilder': 'h',
    'prey': 'p',
    'siroco': 's'
    }

TOTAL_ID_2_SERVER_ID = {v : k for k , v in SERVER_ID_2_TOTAL_ID.items()}

# 서버 ID 문자열 길이의 최대값
SERVERLENGTH = max(list(map(lambda x : len(x), list(SERVER_NAME_2_ID.values()))))

# 직업명
JOBCLASS = {
    "귀검사(남)" : ["웨펀마스터", "버서커", "소울브링어", "아수라", "검귀"],
    "격투가(남)" : ["넨마스터", "스트리트파이터", "그래플러", "스트라이커"],
    "거너(남)" : ["레인저", "메카닉", "런처", "스핏파이어", "어썰트"],
    "마법사(남)" : ["블러드 메이지", "엘레멘탈 바머", "빙결사", "디멘션워커", "스위프트 마스터"],
    "프리스트(남)" : ["크루세이더", "퇴마사", "인파이터", "어벤저"],
    "귀검사(여)" : ["소드마스터", "데몬슬레이어", "다크템플러", "베가본드", "블레이드"],
    "격투가(여)" : ["넨마스터", "스트리트파이터", "그래플러", "스트라이커"],
    "거너(여)" : ["레인저", "메카닉", "런처", "스핏파이어"],
    "마법사(여)" : ["엘레멘탈마스터", "마도학자", "소환사", "배틀메이지", "인챈트리스"],
    "프리스트(여)" : ["크루세이더", "이단심판관", "미스트리스", "무녀"],
    "도적" : ["로그", "쿠노이치", "섀도우댄서", "사령술사"],
    "나이트" : ["엘븐나이트", "카오스", "드래곤나이트", "팔라딘"],
    "마창사" : ["뱅가드", "듀얼리스트", "다크 랜서", "드래고니안 랜서"],
    "총검사" : ["요원", "트러블 슈터", "히트맨", "스페셜리스트"],
    "외전" : ["다크나이트", "크리에이터"],
    "아처" : ["뮤즈", "트래블러", "헌터", "비질란테"]
}

jobclass_list = [item for sublist in list(JOBCLASS.values()) for item in sublist]

# 1차 전직명 문자열 길이의 최대값
JOB_GROW_NAME_LENGTH = max(list(map(lambda x : len(x), jobclass_list)))

# 직업명 문자열 길이의 최대값
JOB_NAME_LENGTH = max(list(map(lambda x : len(x), list(JOBCLASS.keys()))))

del jobclass_list

# 착용가능 장비
EQUIPMENT_LIST = ['total_id', 'weapon', 'title', 'jacket', 'shoulder', 'pants', 'shoes', 'waist', 'amulet', 'wrist', 'ring', 'support', 'magic_ston', 'earring', 'set_item_info']

# 착용가능 아바타
AVATAR_LIST = ['total_id', 'headgear', 'hair', 'face', 'jacket', 'pants', 'shoes', 'breast', 'waist', 'skin', 'aurora', 'weapon']

# 플래티넘 엠블렘 착용 가능 부위
PLATINUM_AVATAR_LIST = ['jacket', 'pants']

# CharacterSearch 에서 선택 가능한 변수
CHARACTER_SEARCH_NAME = {
    'server_id': 'serverId',
    'character_id': 'characterId',
    'character_name': 'characterName',
    'level': 'level',
    'job_id' : 'jobId',
    'job_grow_id' : 'jobGrowId',
    'job_name': 'jobName',
    'job_grow_name': 'jobGrowName',
    'fame': 'fame',
}

# CharacterInformation 에서 선택 가능한 변수
CHARACTER_INFORMATION_NAME = {
    'total_id' : 'total_id',
    'character_id': 'characterId',
    'character_name': 'characterName',
    'level': 'level',
    'job_name': 'jobName',
    'job_grow_name': 'jobGrowName',
    'adventure_name': 'adventureName',
    'guild_id': 'guildId',
    'guild_name': 'guildName'
}

# Status 에서 선택 가능한 변수
STATUS_NAME = {
    'total_id' : 'total_id',
    'character_id': 'characterId',
    'character_name': 'characterName',
    'level': 'level',
    'job_name': 'jobName',
    'job_grow_name': 'jobGrowName',
    'adventure_name': 'adventureName',
    'guild_id': 'guildId',
    'guild_name': 'guildName',    
    'hp': 'HP',
    'mp': 'MP',
    'physical_defense_rate': '물리 방어율',
    'magical_defense_rate': '마법 방어율',
    'strength': '힘',
    'intelligence': '지능',
    'vitality': '체력',
    'spirit': '정신력',
    'physical_attack': '물리 공격',
    'magical_attack': '마법 공격',
    'physical_critical_chance': '물리 크리티컬',
    'magical_critical_chance': '마법 크리티컬',
    'independent_attack': '독립 공격',
    'attack_speed': '공격 속도',
    'casting_speed': '캐스팅 속도',
    'movement_speed': '이동 속도',
    'fame': '모험가 명성',
    'hit_rate': '적중률',
    'evasion_rate': '회피율',
    'hp_recovery': 'HP 회복량',
    'mp_recovery': 'MP 회복량',
    'stiffness': '경직도',
    'hit_recovery': '히트리커버리',
    'fire_element_enhancement': '화속성 강화',
    'fire_element_resistance': '화속성 저항',
    'water_element_enhancement': '수속성 강화',
    'water_element_resistance': '수속성 저항',
    'light_element_enhancement': '명속성 강화',
    'light_element_resistance': '명속성 저항',
    'dark_element_enhancement': '암속성 강화',
    'dark_element_resistance': '암속성 저항',
    'physical_defense': '물리 방어',
    'magical_defense': '마법 방어',
    'attack_power_increase': '공격력 증가',
    'buff_power': '버프력',
    'attack_power_amplification': '공격력 증폭',
    'buff_power_amplification': '버프력 증폭',
    'final_damage_increase': '최종 데미지 증가',
    'cooldown_reduction': '쿨타임 감소',
    'cooldown_recovery_rate': '쿨타임 회복속도',
    'final_cooldown_reduction_rate': '최종 쿨타임 감소율',
    'damage_increase': '데미지 증가',
    'critical_damage_increase': '크리티컬 데미지 증가',
    'additional_damage_increase': '추가 데미지 증가',
    'all_attack_power_increase': '모든 공격력 증가',
    'physical_attack_power_increase': '물리 공격력 증가',
    'magical_attack_power_increase': '마법 공격력 증가',
    'independent_attack_power_increase': '독립 공격력 증가',
    'strength_increase': '힘 증가',
    'intelligence_increase': '지능 증가',
    'damage_over_time': '지속피해',
    'physical_damage_reduction': '물리 피해 감소',
    'magical_damage_reduction': '마법 피해 감소',
    'bleed_damage_conversion': '출혈 피해 전환',
    'poison_damage_conversion': '중독 피해 전환',
    'burn_damage_conversion': '화상 피해 전환',
    'electrocution_damage_conversion': '감전 피해 전환',
    'bleed_resistance': '출혈 내성',
    'poison_resistance': '중독 내성',
    'burn_resistance': '화상 내성',
    'electrocution_resistance': '감전 내성',
    'freeze_resistance': '빙결 내성',
    'slow_resistance': '둔화 내성',
    'stun_resistance': '기절 내성',
    'curse_resistance': '저주 내성',
    'darkness_resistance': '암흑 내성',
    'petrification_resistance': '석화 내성',
    'sleep_resistance': '수면 내성',
    'confusion_resistance': '혼란 내성',
    'restraint_resistance': '구속 내성',
    'fire_element_damage': '화속성 피해',
    'water_element_damage': '수속성 피해',
    'light_element_damage': '명속성 피해',
    'dark_element_damage': '암속성 피해',
    'bleed_damage': '출혈 피해',
    'poison_damage': '중독 피해',
    'burn_damage': '화상 피해',
    'electrocution_damage': '감전 피해'
 }

GROWINFO_NAME = {
        "level" : "level",
        "exp_rate" : "expRate",
        "option" : "options"
}


BASE_EQUIPMENT_NAME = {
    'item_name' :'itemName',
    'item_available_level' :'itemAvailableLevel',
    'item_rarity' :'itemRarity',
    'reinforce' :'reinforce',
    'amplification_name' :'amplificationName',
    'refine' :'refine', 
    'item_grade_name' :'itemGradeName',
    'enchant' : 'enchant'
}

EQUIPMENT_NAME = {
    'upgrade_info' : 'upgrade_info',
    'mist_gear' :  'mist_gear',
    'grow_info' : 'grow_info'
}

WEAPON_NAME = {
    'bakal_info' : 'fusionOption',
    'asrahan_info':'asrahanOption'
}

AVATAR_NAME = {
        'item_name' : "itemName",
        'item_rarity' : "itemRarity",
        'option_ability' : "optionAbility",
        'emblems' : 'emblems'
}

PLATINUM_AVATAR_NAME = {
        'item_name' : "itemName",
        'item_rarity' : "itemRarity",
        'option_ability' : "optionAbility",
        'emblems' : 'emblems',
        'platinum_emblem' : 'emblems'
}