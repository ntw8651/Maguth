from sprites import *
from maths import *
from settings import *
#대략 스킬마다 다 발동하는 느낌이 다를거아냐 음 근데 이러면 여기서 고친게 main이랑 다를텐데
#NEED ADD AND FIX : 나중에 damageType에 

'''
tab : 탭 구분 (physical, magical)
name : 표시될 이름

require : 필요 조건
cost : 소모 코스트
target : 스킬 대상 구분 (enemy, player)
type : 스킬 구분 (damage : 데미지 가함(*힐의 경우 음수), buff : 온갖 상태이상, parrying : 패링(흘리기), block : 막기 )
damageType : 데미지 타입 구분 (physical 물리데미지, magical 마법데미지, true 고정데미지)
damageStatus : 데미지 배율 str : 0.6 ->> str스탯의 0.6배만큼 데미지에 합산
isEnd : 스킬 끝?~
isAttacking : True일 경우 다음 틱에 현재 저장된 값으로 공격함
skillCount : 현재 스킬 카운트 여러스킬 이어서 발동에 사용
particles : 파티클들
sfx : 효과음
formula : 수식
success : 성공여부


스킬
참고 : 
- 막기랑 패링의 차이 : 막기는 데미지 감소, 패링은 데미지 무효. 난이도 : 막기 < 패링..., -> 패링은 마법과 물리 둘 중 하나로 한정 (마법 무효(마법패링), 패링(물리패링))
'''

class S_Smash():
    def __init__(self):
        self.tab = 'physical'
        self.name = '대각베기'
        self.require = [{}]
        self.cost = {'stamina' : 1}
        self.target = "enemy" #or magical
        self.type = "damage"
        self.damageType = 1
        self.isEnd = False
        self.isAttacking = False
        self.damageStatus = {}
        self.skillCount = 0
        self.particles = []
        self.sfx = ''
        self.timeDelay = 0
        self.success = True
        self.formula = []
        self.penalty = [{}]

    
    def OnSkill(self, player):
        if(self.isAttacking == False):
            if(self.skillCount == 0):
                self.NormalAttack(player)
            else:
                self.End()
            self.skillCount += 1
        self.isAttacking = True
        

    def NormalAttack(self, player):
        self.type = "damage" #or magical 
        self.damageType = 'physical'
        self.damageStatus = {"damage": player.str * 10,'random':[90, 110]}
        self.dialog = ['']
        self.sfx = 'bash_2'
        self.formula = [M_add(1, 2, 1)]
        self.penalty = [{}]

    def End(self):
        self.__init__()
        self.isEnd = True
#NEED ADD : 스킬창, 스킬 코스트 설명등등 볼 수 있게 추가

class S_QuadraSpire():
    def __init__(self):
        self.tab = 'physical'
        self.name = '사연격'
        self.require = [{}]
        self.cost = {'stamina' : 10}
        self.target = "enemy" #or player
        self.type = "damage"
        self.damageType = "physical"
        self.isEnd = False
        self.isAttacking = False
        self.damageStatus = {}
        self.skillCount = 0
        self.particles = []
        self.sfx = ''
        self.timeDelay = 0
        self.success = True
        self.formula = []
        self.penalty = [{}]

    
    def OnSkill(self, player):
        if(self.isAttacking == False):
            if(self.skillCount < 3):
                self.SlashAttack(player)
            elif(self.skillCount < 4):
                self.SpireAttack(player)
            else:
                self.End()
            self.skillCount += 1
        self.isAttacking = True
        

    def SlashAttack(self, player):
        self.type = "damage" 
        self.damageType = 'physical'
        self.damageStatus = {"damage": player.str * 5, "random": [90, 110]}
        self.dialog = ['§l§0\"흡!\"', '§l§0\"합!\"', '§l§0\"핫!\"']
        self.formula = [M_add(1, 2, 1)]
        self.penalty = [{}]

    def SpireAttack(self, player):
        self.type = "damage"
        self.damageType = 'physical'
        self.damageStatus = {"str": 1, "damage": player.str * 10, "random": [90, 140]}
        self.dialog = ['§l§0\"받아라!\"', '§l§0\"흐아앗!\"', '§l§0\"으랴앗!\"']
        self.formula = [M_add(1, 3, 0)]
        self.penalty = [{}]

    def End(self):
        self.__init__()
        self.isEnd = True

class S_RandomlySwing():
    def __init__(self):
        self.tab = 'physical'
        self.name = '마구 휘두르기'
        self.require = [{}]
        self.cost = {'stamina' : 10}
        self.target = "enemy" #or player
        self.type = "damage"
        self.damageType = "physical"
        self.isEnd = False
        self.isAttacking = False
        self.damageStatus = {}
        self.skillCount = 0
        self.particles = []
        self.sfx = ''
        self.dialog = []
        self.timeDelay = 0
        self.success = True
        self.formula = []
        self.penalty = [{}]

    
    def OnSkill(self, player):
        if(self.isAttacking == False):
            if(self.skillCount < 1):
                self.SkillFormula()
            elif(self.skillCount < 5):
                self.NormalAttack(player)
            else:
                self.End()
            self.skillCount += 1
        self.isAttacking = True
    
    def SkillFormula(self):
        self.formula = [M_add(1, 2, 0)]

    def NormalAttack(self, player):
        self.sfx = 'bash_2'
        self.type = "damage" #or magical 이걸 기본적으로 여러 formula를 이용해서 때릴까... 아니면 하나만 풀면 자동으로 따따따 떄리게 할까... 둘다 가능하게 완료
        self.damageType = 'physical'
        self.damageStatus = {"damage": player.str * 5, 'random':[70, 110]}
        self.dialog = ['§l§0\"핫!\"', '§l§0\"슥!\"', '§l§0\"합!\"']
        self.penalty = [{}]
        self.timeDelay = 0.5 * TICK_PER_SEC

    def End(self):
        self.__init__()
        self.isEnd = True

class S_DebugKill():
    def __init__(self):
        self.tab = 'physical'
        self.name = '디버그-킬'
        self.require = [{}]
        self.cost = {'stamina' : 1}
        self.target = "enemy" #or magical
        self.type = "damage"
        self.damageType = 1
        self.damage = [{"normal": 0.1}]
        self.isEnd = False
        self.isAttacking = False
        self.damageStatus = {}
        self.skillCount = 0
        self.particles = []
        self.sfx = ''
        self.timeDelay = 0
        self.success = True
        self.formula = []
        self.penalty = [{}]

    
    def OnSkill(self, player):
        if(self.isAttacking == False):
            if(self.skillCount == 0):
                self.NormalAttack()
            else:
                self.End()
        self.isAttacking = True
        

    def NormalAttack(self):
        self.type = "damage" #or magical 
        self.dialog = ['§7"치트의 맛을 봐라!"']
        self.damageType = 'physical'
        self.damageStatus = {"damage": 20050217}
        self.skillCount += 1
        self.formula = [M_add(1, 2, 1, 2)]
        self.penalty = [{}]

    def End(self):
        self.__init__()
        self.isEnd = True

class S_Block():
    def __init__(self):
        self.tab = 'physical'
        self.name = '막기'
        self.require = [{}]
        self.cost = {'stamina' : 1}
        self.target = "self"
        self.type = "block"
        self.damageType = 1
        self.damage = [{"normal": 0.1}]
        self.isEnd = False
        self.isAttacking = False
        self.damageStatus = {}
        self.skillCount = 0
        self.particles = []
        self.sfx = ''
        self.timeDelay = 0
        self.success = True
        self.formula = []
        self.penalty = [{}]

    
    def OnSkill(self, player):
        if(self.isAttacking == False):
            if(self.skillCount == 0):
                self.NormalAttack()
            else:
                self.End()
        self.isAttacking = True
        

    def NormalAttack(self):
        self.type = "buff" #or magical 
        self.dialog = ['§l§7당신은 방어에 신경씁니다!']
        self.damageType = 'physical'
        self.damageStatus = {}
        self.skillCount += 1
        self.formula = [M_add(2, 2, 1)]
        self.penalty = [{}]
        self.effects = [{'name' : 'blocking', 'tick' : 4*TICK_PER_SEC}]

    def End(self):
        self.__init__()
        self.isEnd = True

class S_Parry():#NEED ADD : 코스트 처리
    def __init__(self):
        self.tab = 'physical'
        self.name = '검흘리기'
        self.require = [{}]
        self.cost = {'stamina' : 1}
        self.target = "self" #or magical
        self.type = "buff"
        self.damageType = 1
        self.damage = [{"normal": 0.1}]
        self.isEnd = False
        self.isAttacking = False
        self.damageStatus = {}
        self.skillCount = 0
        self.particles = []
        self.sfx = ''
        self.timeDelay = 0
        self.success = True
        self.formula = []
        self.penalty = [{}]

    
    def OnSkill(self, player):
        if(self.isAttacking == False):
            if(self.skillCount == 0):
                self.Parry()
            else:
                self.End()
            self.skillCount += 1
        self.isAttacking = True
        

    def Parry(self):
        self.type = "buff" #or magical
        self.damageType = 'physical'
        self.damageStatus = {}
        self.dialog = ['§l§7당신은 공격에 반응하고자 노력합니다!']
        self.formula = [M_add(1, 3, 0)]
        self.penalty = [{}]
        self.effects = [{'name' : 'parrying', 'tick' : 1.5*TICK_PER_SEC}]

    def End(self):
        self.__init__()
        self.isEnd = True