import pygame as pg
import random
from skills import *
from items import *
from settings import *
from custom_operator import *
#플레이어는 굳이 뭐 움직이지도 뭘 하지도 않는데 스프라이트로 줄 필요가 있나?
#그냥 전역변수로써 쓰면 되지 않을까? 그 여기서 가져오는게 self 지정을 하는건 딴데서 부르기 위해서 쓰는거니까 딱히 안넣어두 되겠지?
#어? 그냥 이벤트도 여기다 저장하면 나중에 게임 저장시에 Player만 저장하면 되는 거..아닌...가?
#아 이거 좀 고민되네... 문제를 다 풀고 공격이냐 문제 풀면서 공격이냐아니지 그냥 둘다 있으면 되는거잖아
# value_t : _t는 temp, 즉 전투시에 값을 받아와서 사용하는 값
class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        
        #없어도 될듯
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)

        self.maxHealth = PRE_PLAYER_HEALTH
        self.health = PRE_PLAYER_HEALTH


        self.shield = PRE_PLAYER_SHIELD

        self.focus = PRE_PLAYER_FOCUS
        self.stamina = PRE_PLAYER_STAMINA

        self.focus_t = self.focus
        self.stamina_t = self.stamina

        self.str = PRE_PLAYER_STR
        self.int = PRE_PLAYER_INT
        self.dex = PRE_PLAYER_DEX
        self.wis = PRE_PLAYER_WIS
        
        self.spelltime = PRE_PLAYER_SPELLTIME
        self.effects = PRE_PLAYER_EFFECTS
        self.money = PRE_PLAYER_MONEY
        self.items = [{'item' : I_HealPotion(), 'amount' : 1}, 
                      {'item' : I_HealPotion(), 'amount' : 1}, 
                      {'item' : I_HealPotion(), 'amount' : 1}, 
                      {'item' : I_HealPotion(), 'amount' : 1}, 
                      {'item' : I_Poo(), 'amount' : 1},
                    ]
        self.worldValue = {}
        
        self.timeScale_t = 1
        self.timeScale = 1

        self.feats = []
        #아 근데 플레이어 접근할 수 있어야 될 것 같은데 좀 그래야 엄청 수월해지고... 오키 그냥 연결시키자
        
        self.skills = {1 : S_Smash(),  
                       2 : S_RandomlySwing(),
                       3 : S_Block(), 
                       4 : S_Parry(),
                      }
        #BattleState
        self.blockingTick = 0
        self.parryingTick = 0
        self.run = False
        self.resistPhysical = 0

    
    #월드 값 다루기
    def SetWorldValue(self, _name, _value):
        self.worldValue[_name] = _value

    def ModifyWorldValue(self, _name, _value):
        if(_name in self.worldValue):
            self.worldValue[_name] += _value
        else:
            self.SetWorldValue(_name, _value)
    
    def GetWorldValue(self, _name):
        if(_name in self.worldValue):
            return self.worldValue[_name]
        else: 
            return 0 

    #전투 초기화
    def BattleStartInital(self):
        self.timeScale_t = self.timeScale
        self.guardTick = 0
        self.parryingTick = 0
        self.run = False

    #전투시 지속 발동(전투 처리)
    def UpdateBattle(self):
        #틱 업데이트
        if(self.blockingTick > 0):
            self.blockingTick -= 1
            self.shield = 3 #NEED FIX : 방패 능력치에 따라 방어 효율 설정하게 변경

        if(self.parryingTick > 0):
            self.parryingTick -= 1

    #NEED FIX : 플레이어도 방어력(쉴드 말고) 추가
    def GetDamage(self, _damage, _type = 'normal'):
        if(_type == 'normal'):
            if(self.shield >= _damage):
                self.shield -= _damage
            else:
                self.health -= _damage - self.shield
                self.shield = 0
        elif(_type == 'true'):
            self.health -= _damage
    
    def GetHeal(self, _value):
        if(_value > self.maxHealth - self.health):
            _value = self.maxHealth - self.health

        self.health += _value
        return _value


    def EffectCheck(self):
        _selection = 0 
        for i in self.effects:
            _effect = i
            if(_effect["name"] == 'adictied'):
                self.health -= _effect["damage"]

            self.effects[_selection]["duration"] -= 1
            if(self.effects[_selection]["duration"] <= 0):
                del self.effects[_selection]
                _selection -=1

            _selection += 1
                
                


class M_TutorialTree(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load(IMAGE_PATH + "Tree_1.png").convert_alpha()
        
        self.bgm = 'normal_enemy'

        self.scaled_width = self.image.get_width() * 6
        self.scaled_height = self.image.get_height() * 6
        self.image = pg.transform.scale(self.image, (self.scaled_width, self.scaled_height))


        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)#position


        self.name = "나무"
        self.maxHealth = 250
        self.health = self.maxHealth
        self.shield = 0
        #쿨타임 최대 및 속도. 최대값이 작을수록 바가 빨리 줄어들음. 바가  음... 일단 그냥 설정해두는 걸로...
        self.maxCooltime = 10*TICK_PER_SEC # 10초
        #첫 공격 어택 쿨타임. 그 다음 공격부턴
        self.attackCooltime = 10*TICK_PER_SEC
        self.effects = []
        self.isAttacking = False
        self.isBuffing = False
        self.loots = [{'item' : I_WoodStick(), 'min' : 1, 'max' : 2},]

        self.description = f'§l§0{self.name} : 이름은 나무고, 오늘 당신의 도끼질 연습 샌드백입니다. 그런데 뭐라고 중얼거리는 것 같기도 합니다...'
        self.resistPhysical = 0.1
        self.resistMagical = 0
        self.resistFire = 0
        self.resistIce = 0

        #for enemy skill
        self.skillName = ''
        self.skillDamage = 0
        self.skillElemental = 'normal'
        self.skillType = 'damage'
        self.skillDamageType = 'physical'
        self.isEscapable = False
        self.escapeMsg = '§l§0잠깐... 나무 베야죠!' 
    




    def Battle(self):
        if(self.attackCooltime < 0):
            enemyAttack = random.choices([self.NormalAttack],[0.5])[0]
            enemyAttack()
            

    def NormalAttack(self):

        self.skillName = '살랑거리기'
        self.skillDamage = 0
        self.skillElemental = 'normal'
        self.skillType = 'buff'
        self.skillDamageType = 'physical'
        self.skillDialog = '\'숫자... 입력... 계산...\' 마치 그렇게 중얼거리는 것 같습니다.'

        self.attackCooltime = 8*TICK_PER_SEC#장실
        
        self.isAttacking = True
    

    #애니메이션은 좀 시간이 걸릴 듯 하니 미완성 NEED ADD : enemy 공격 애니메이션 제작
    def AttackAnimation(self, tick_counter):
        C_Delay(self.skillName, tick_counter, 0.8)
        if(C_GetDelay(self.skillName)['time'] < C_GetDelay(self.skillName)['length']):
            _percent = (C_GetDelay(self.skillName)['time'] / C_GetDelay(self.skillName)['length'])
            self.scaled_width_ani = self.scaled_width * (1 + 0.5 * _percent)
            self.scaled_height_ani = self.scaled_height * (1 + 0.5 * _percent)
            self.image = pg.transform.scale(self.image, (self.scaled_width_ani, self.scaled_height_ani))
    





#과연 이걸 몹마다 따로 클래스를 지정해줘야할까? 같은 적이 두번이상 등장할 것인가?
#음 등장할 것이다 그럼..뭐... 따로 해야지 않겄어
#이게 굳이 스프라이트가 필요하지 음음 아마 필요할테지
#아 그러네 저기다 이미지로 그릴 필요 없이 스프라이트로 넣으면 되는구나
class M_PariahDog(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load(IMAGE_PATH + "WolfBoss.png").convert_alpha()
        
        self.bgm = 'normal_enemy'

        scaled_width = self.image.get_width() * 3
        scaled_height = self.image.get_height() * 3
        self.image = pg.transform.scale(self.image, (scaled_width, scaled_height))


        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)#position


        self.name = "야생 들개"
        self.maxHealth = 200
        self.health = self.maxHealth
        self.shield = 0
        #쿨타임 최대 및 속도. 최대값이 작을수록 바가 빨리 줄어들음. 바가  음... 일단 그냥 설정해두는 걸로...
        self.maxCooltime = 5*TICK_PER_SEC # 10초
        #첫 공격 어택 쿨타임. 그 다음 공격부턴
        self.attackCooltime = 5*TICK_PER_SEC
        self.effects = []
        self.isAttacking = False
        self.isBuffing = False


        self.description = f'§l§0{self.name} : 상당히 늑대를 닮았지만, 야생 개입니다. 어째서인지 이빨을 보이고 있습니다. 물리면 꽤나 아플 것 같습니다.'
        self.resistPhysical = 0.1
        self.resistMagical = 0
        self.resistFire = 0
        self.resistIce = 0

        #for enemy skill
        self.skillName = ''
        self.skillDamage = 0
        self.skillElemental = 'normal'
        self.skillType = 'damage'
        self.skillDamageType = 'physical'

    def Battle(self):
        if(self.attackCooltime < 0):
            enemyAttack = random.choices([self.NormalAttack, self.Bite],[0.5, 0.5])[0]
            enemyAttack()
            
    def NormalAttack(self):
        self.skillName = '할퀴기'
        self.skillDamage = 2
        self.skillElemental = 'normal'
        self.skillType = 'damage'
        self.skillDamageType = 'physical'

        self.attackCooltime = 1*TICK_PER_SEC
        self.isAttacking = True
    
    def Bite(self):

        self.skillName = '물어뜯기'
        self.skillDamage = 6
        self.skillElemental = 'normal'
        self.skillType = 'damage'
        self.skillDamageType = 'physical'

        self.attackCooltime = 3*TICK_PER_SEC
        self.isAttacking = True

class M_Phantom(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load(IMAGE_PATH + "You.png").convert_alpha()
        
        self.bgm = 'boss'

        scaled_width = self.image.get_width() * 4
        scaled_height = self.image.get_height() * 4
        self.image = pg.transform.scale(self.image, (scaled_width, scaled_height))


        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)#position


        self.name = "악령"
        self.maxHealth = 800
        self.health = self.maxHealth
        self.shield = 0
        #쿨타임 최대 및 속도. 최대값이 작을수록 바가 빨리 줄어들음. 바가  음... 일단 그냥 설정해두는 걸로...
        self.maxCooltime = 5*TICK_PER_SEC # 10초
        #첫 공격 어택 쿨타임. 그 다음 공격부턴
        self.attackCooltime = 5*TICK_PER_SEC

        #name, value, tick
        self.effects = []
        
        self.isAttacking = False
        self.isBuffing = False


        self.description = f'§l§1{self.name} : ����이 ����������지 ���' #일부러
        self.resistPhysical = 0.1
        self.resistMagical = 0
        self.resistFire = 0
        self.resistIce = 0

        #for enemy skill
        self.skillName = ''
        self.skillDamage = 0
        self.skillElemental = 'normal'
        self.skillType = 'damage'
        self.skillDamageType = 'physical'
        self.isEscapable = False
        self.escapeMsg = '§l§1못%(#!ㄱ@%ㅏ$' 






    def Battle(self):
        if(self.attackCooltime < 0):
            enemyAttack = random.choices([self.Smash, self.Impale, self.Guard],[0.5,0.3, 0.2])[0]
            enemyAttack()

        #NEED FIX : 이거... 상당히 맘에 안 들음. 나중에 손보기로 대략 방향성은... 매 프레임 계산 안하기... 정도 그리고 틱마다로 묶는거 말고... 대략... 미래의 내가
        #잘 알아서 하겠지 ㅎㅎ...
        #effects : -> name, tick, value NEED FIX value...이거
        for i in range(len(self.effects)):
            if(self.effects[i]['tick'] > 0):
                self.effects[i]['tick'] -= 1
                #상태 체크
                if(self.effects[i]['name'] == 'guard'):
                    self.resistPhysical = 0.6


            if(self.effects[i]['tick'] <= 0):
                if(self.effects[i]['name'] == 'guard'):
                    self.resistPhysical = 0.1
                    
        #개별적 상태
            
    #NEED FIX : 차라리 CoolTime을 뒤가 아니라 앞으로 넣어서 플레이어가 공격을 유추할 수 있게 하는 게 나을듯? 수정하기
    def Smash(self):
        self.skillName = '#@$기'
        self.skillDamage = 8
        self.skillElemental = 'normal'
        self.skillType = 'damage'
        self.skillDamageType = 'physical'
        self.skillDialog = '§l§1"%쓰%#$(!"'
        self.attackCooltime = 1.5*TICK_PER_SEC
        self.isAttacking = True
    
    def Impale(self):
        self.skillName = '찌?$@'
        self.skillDamage = 22
        self.skillElemental = 'normal'
        self.skillType = 'damage'
        self.skillDamageType = 'physical'
        self.skillDialog = '§l§1"안%)#(!$#)"'
        self.attackCooltime = 3*TICK_PER_SEC
        self.isAttacking = True
    

    def Guard(self):
        self.skillName = '$막?'
        self.skillDamage = 0
        self.skillElemental = 'normal'
        self.skillType = 'buff'
        self.skillDamageType = 'physical'
        self.skillDialog = '§l§3악령이 방어 자세를 잡았다.'
        self.attackCooltime = 5*TICK_PER_SEC
        self.isAttacking = True
        self.effects.append({'name': 'guard', 'tick': 5*TICK_PER_SEC, 'value': 1})

player = Player(pg)