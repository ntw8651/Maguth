
'''
tools list
Cutting : 나무 자르는 힘
Mining : 광물캐는 힘
Mowing : 풀 베는 힘
Digging : 땅파는 힘


'''

'''
각 요소
name : 표시
id : 나중에 이름이 바뀌어도(번역) 대조를 위해
tools : 도구파워(카타클)
itemType : Weapon, Armor, Material(소재) 등등... 아이템 타입 확인. Weapon과 Tool는 둘다 무기로 들기는 가능
damage : 모든 타입 공격력들 딕셔너리로 입력
damageType : 물리 공격 or 마법 공격 or 두가지 모두
elemetnalType : 원소 타입
아 일단 처음에는 수학으로 싸우는 걸 표방은 했지만 마법만 쓰는 건 아니게 될 것 같네 하다보니까 세상엔 음음 마검사도 있는 법이니까


'''


#무기 및 도구(장착 및 공격 가능)
class I_BluntAxe():
    def __init__(self):
        self.name = "무딘 도끼"
        self.id = 0
        self.tools = [{'name' : 'Axe', 'level' : 3}]
        
        self.itemType = 'Weapon'

        self.damage = [{'name' : 'physical', 'damage' : 5}, 
                       {'name' :'magical', 'damage' : 0}, 
                       {'name' : 'elemental', 'damage' : 0}]

        self.effects = [{}]
        
class I_WoodenSword():
    def __init__(self):
        self.name = "목검"
        self.id = 1
        self.tools = [{'name' : 'Axe', 'level' : 3}]
        self.description = "굉장히 "
        self.itemType = 'Weapon'


        self.damageType = 'physical'  #physical, magical, both
        self.elementalType = 'normal'
        self.physicalDamage = 6
        self.magicalDamage = 0
        self.elemetnalDamage = 0
        self.effects = [{}]

class I_WoodenWand():
    def __init__(self):
        self.name = "나무 마법봉"
        self.description = "아직 이 아이템은 얻을 수 없는데"
        self.id = 2
        self.tools = [{'name' : 'Axe', 'level' : 3}]
        self.itemType = 'Weapon'
        self.damageType = 'physical'  #physical, magical, both

        self.effects = [{}]
    
#재료 아이템
class I_WoodStick():
    def __init__(self):
        self.name = "나뭇가지"
        self.id = 201
        self.tools = [{}]
        
        self.itemType = 'Material'

        self.description = "무수히 유용합니다."


        self.effects = [{}]
        self.droppable = True

class I_Poo():
    def __init__(self):
        self.name = "퍼런 쓰레기"
        self.id = 202
        self.itemType = 'Material'
        self.description = "'파랗고, 쓸모없습니다.'"

#소비 아이템
class I_HealPotion():
    def __init__(self):
        self.name = "붉은 물약"
        self.id = 401
        self.tools = [{}]
        #데미지 = 불데미지, 이펙트 = 화상
        self.damage = []
        #화상을 입히는 것과 불 데미지를 입히는 것 다름
        self.effects = [{'name' : 'heal', 'value' : 30}]
        self.description = "체력을 회복시킵니다."
        self.itemType = 'Consumable'
        self.maxAmount = 9
        self.target = 'self'
        self.droppable = True
        self.elementalType = 'normal'