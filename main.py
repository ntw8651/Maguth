import pygame as pg
from pygame import mixer
import sys
from pygame.locals import QUIT

from settings import *
from sprites import *
from maths import *
from custom_operator import *
from dialogs import *
from events import *
from skills import *

import asyncio
import time
import random
import re
import copy as cp
'''
re.sub('[^가-힣\s]', '', text)

예: 한글만 추출하기
string = "1-----(사람)!@   1"
re.sub('[^A-Za-z가-힣]', '', string)   
'사람'
'''
from random import randrange

'''
추가 및 고칠 것

- 어드벤쳐 화면 -> 전투 화면
- 전투
=> 이거 완전 실-시간 전투


며칠 안 남았으니 할 것
오늘 안에 할 것
진짜 마지막으로 넣을 것 : 스탯창, ...머 그정도 그리고 팬텀 공격 퍼센트 조절

밭 싸우기, 촌장 말걸기, 아이템 쓰기 물약O, 도망치기, 스탯보기


동굴 보스전 및 베타 엔딩 (이야기가 아직 다 안 쓰였는 걸...라는 엔딩)
마법 및 방어 그리고 상점에서 물건 삽삽
사냥터 만들기
퀘스트 만들기
스킬 만들기
아이템 얻기 
+
밑에 것들 대략 현존 버그는 말살된 듯

- 마법 발동
- 다른 마법들
O 이벤트 제작
O 이벤트 효과 적용 함수 제작 eventEffectApply
O 아이템 제작
- 실패 패널티 적용
O 전투 dialog
- 인벤창 만들기 인벤은... 0으로 가보자  0으로 이것저것 하는 창 꺼내고 인벤창, 스킬창, 스탯창, 끄기,
- 공격 이펙트 및 적 흔들림
- 전투 UI (체력 정신력 등등)
- 집중력 시스템 : 문제 푸는 시간. 문제 푸는 시간이 너무 느리면 못싸움! focus


- 나중 추가 기능;
- 스킬 체인 : 기술 묶어서 전체 기술 수식 다 풀어야 발동, 도중 공격 및 틀리면 실패, 데미지 가산 100% + n * 20%
- 특정 기술 묶을 시 추가효과
- 마법진 에니메이션 및 이펙트 -> 물리공격은 선 긋기(검모양 원의 원주를 나눠서) 마법 공격은 동그라미 서클 쌓이게 버프는 뭐... 십자가 모양?
- 그리고 또 원소 부여는 뭐 색깔 입히기로 하고 기대가 된다


이벤트큐 -> [이벤트, 카운트] 카운트 0 될때까지 쪼금씩 내리고, 만약 카운트가 0이 되었다
조건 검사, 조건 불충분시 랜덤 카운트 추가 1~5턴
조건 충족시 해당 이벤트 실행(pop)

좀 질리니까 이번엔 딴데 손보자 ㅎㅎ...

'''



'''
Class and Def Prefix

P_ 장면, 화면, 씬 전투화면 메인화면 등등...함수
S_ 마법(Spell)과 기술(Skill)
E_ 이벤트class
M_ 몬스터들(적)
I_ 아이템들

'''
#Starting Point, Global Value,


#Game Starter
#대문자 = 상수
pg.init()
pg.display.set_caption('SHOOT_GAME')#창 이름
O_SURFACE = pg.display.set_mode((WIDTH,HEIGHT))
SURFACE = O_SURFACE.copy()
O_SURFACE = pg.display.set_mode((O_WIDTH, O_HEIGHT))
FPSCLOCK = pg.time.Clock()

#Sound Starter
mixer.init()



title_font = pg.font.SysFont(None, 40)
enemy_name_font = pg.font.Font(KOR_FONT, 40)
formula_font = pg.font.Font(KOR_FONT, 30)
dialog_font = pg.font.Font(KOR_FONT, 22) #여기까지 하고 숙제때매 이만...
battle_log_font = pg.font.Font(KOR_FONT, 20)

info_font_large = pg.font.Font(KOR_FONT, 40)
info_font_medium = pg.font.Font(KOR_FONT, 32)
info_font_small = pg.font.Font(KOR_FONT, 22)


system_font_large = pg.font.Font(KOR_FONT, 50)
system_font_medium = pg.font.Font(KOR_FONT, 40)
system_font_small = pg.font.Font(KOR_FONT, 30)
tick_counter = 0


#각 페이지에서 사용하는 일종의 temp, 페이지 전환시마다 0으로 초기화 시켜줄 것.
general_control_state = 0


#ui image
health_bar = pg.image.load(HEALTH_BAR_PATH)
health_bar_case = pg.image.load(HEALTH_BAR_CASE_PATH)

health_bar = pg.transform.scale(health_bar, (health_bar.get_width() * 2.5, health_bar.get_height()/2))
health_bar_case = pg.transform.scale(health_bar_case, (health_bar_case.get_width() * 2.5, health_bar_case.get_height()/2))


#btn image
btn_battle_magic = pg.image.load(BTN_BATTLE_MAGIC_PATH)
btn_battle_magic = pg.transform.scale(btn_battle_magic, (btn_battle_magic.get_width()*1.25, btn_battle_magic.get_height()*1.25))

btn_battle_magic_highlight = pg.image.load(BTN_BATTLE_MAGIC_HIGHLIGHT_PATH)
btn_battle_magic_highlight = pg.transform.scale(btn_battle_magic_highlight, (btn_battle_magic_highlight.get_width()*1.25, btn_battle_magic_highlight.get_height()*1.25))
#
btn_battle_check = pg.image.load(BTN_BATTLE_CHECK_PATH)
btn_battle_check = pg.transform.scale(btn_battle_check, (btn_battle_check.get_width()*1.25, btn_battle_check.get_height()*1.25))

btn_battle_check_highlight = pg.image.load(BTN_BATTLE_CHECK_HIGHLIGHT_PATH)
btn_battle_check_highlight = pg.transform.scale(btn_battle_check_highlight, (btn_battle_check_highlight.get_width()*1.25, btn_battle_check_highlight.get_height()*1.25))



#CHECK FPS
clock = pg.time.Clock()

running = True
frame_count = 0
start_time = pg.time.get_ticks()






is_player_turn = False
#그럼 도대체 값을 어떻게 변경하지


#for spell
spell_maker_count = 0
spell_maker_count_max = PRE_PLAYER_MAXSPELL
spell_result = {
    "damage" : 0,
    "level" : 0,
    "type" : "normal",
    "effects" : {},
    "target" : "self",
}

#for misic function...
is_enemy_hit = False
enemy_hit_count = -100
now_bgm = ''
is_reverse_wheel = False



#for input Function
is_input_all = True # for "any key"
is_input_start = False
is_input_end = False
is_input_wheel = False
is_input_num_minus = False
input_wheel = 0
input_number = 0
input_number_str = ''
input_number_length = 9
is_input_backspace = False


#page Setting
now_page_state = 0 #page_state... 0,1,2... [MainPage(booting Game), AdvanturePage, CombatPage, ...]
next_page_state = 0

#ForChangeDisplay... 'is' is arrow "bool"
is_changing_page_state = False
is_page_change_on = False
page_change_count = 10


is_draw_formula = False

#spellContainer
spell_queue = [[]]

#spellCircle
#image Setting
circle_arr = [
                ]


#for P_Mainmenu
is_any_key_pressed = False
any_key_pressed_tick = 0


#for P_Adventure
event_tick = 0

'''
0: left Bar on
1: 인벤토리창
2: 그냥 이것도 general state를 쓸...아니다 이건 딴데서도 쓰니까 이게 나을듯
'''
info_window_state = 0
item_list = []
info_scroll_count = 0


#for P_Battle
battle_log = ['','','','','','','','']
battle_log_tick = 0

highlight_btn_num_for_sfx = 0 #in P_BattleDraw



#coroutine... is don't use
loopC = asyncio.get_event_loop()



#아 진짜 _섞어쓴느거 먼가 맘에 안드는데 또 이래야 잘 보이긴 잘보이고 음... 변수에 _쓰고 함수에는 WasdfOfas식으로 가자 
#아 근데 접근하기 좀 그러니까 그냥 이건 나주엥 따로 저장하는걸로
all_sprites = pg.sprite.Group()
enemy = None

#현재 이벤트 
event = E_Tutorial()
#
skill = None



#EventStack을... 만들까 아니 필요가 없을까 음... 그거다 stack에 채워지기 전에 call해서 random이벤트가 발동하는거야
event_stack = []
event_randoms = [], []
#지난 이벤트
last_event = None


def GameBorder():
    '''
    화면 구분선 그리기
    '''
    Start_Point = [(WIDTH//5*2,0)]
    End_Point = [(WIDTH//5*2, HEIGHT)]
    for index in range(len(Start_Point)):
        pg.draw.line(SURFACE,(255,255,255),Start_Point[index],End_Point[index], 3)

#각 화면을 여따 구성하자 이 구성을 쭉 유지할까 그냥? 아니 2대3 음...
        #전투 화면에서는 대충 이케ㅐ 쓰고 또 특성같은건 마우스 올리면 왼쪼겡 보여주고 그런 식으로 하면
        #얼추 그대로 갈 수 있을듯? 그럼 유아이도 막 크게 바꿀 필요 없으니까 좋고 음음 이 밑에 함수는
        #그 위에 추가로 그려주는 걸 하면 될듯
#스프라이트를 배열에다가 넣어두고 쓰는구나 아 배열에 넣어둬야 충돌체크하고 그럴 때 전체 검사돌리니까 그런건가? 음음 

def InputNumber():#um... NEED DELETE
    if(is_input_start):#End로 처리하고 Start로 받고 음음 그러면 되겠구만
        text_surface = formula_font.render(input_number_str, True, (255, 255, 255))
        SURFACE.blit(text_surface, (WIDTH//5*1 - text_surface.get_width()//2, 
            HEIGHT//2 - text_surface.get_height()//2))


#State Draw Function
def DrawEnemyCooltimeBar(_cooltime_max, _cooltime, _height):
    _now_cooltime_size = (_cooltime/_cooltime_max)
    _rect = pg.Rect(COOLTIME_BAR["pos_x"] - COOLTIME_BAR["size_x"]* _now_cooltime_size/2, _height + COOLTIME_BAR["size_y"], 
                    COOLTIME_BAR["size_x"] * _now_cooltime_size, COOLTIME_BAR["size_y"])
    pg.draw.rect(SURFACE, WHITE, _rect)
    _time = str(round(_cooltime/TICK_PER_SEC, 1))
    _time_text = enemy_name_font.render(_time, True, BLACK)
    SURFACE.blit(_time_text, (COOLTIME_BAR["pos_x"] - _time_text.get_width()/2, _height + COOLTIME_BAR["size_y"]))

def DrawEnemyHealthBar(_Health, _MaxHealth, _Height):
    pos = (WIDTH//5*2+(WIDTH//5*3)/2-(health_bar_case.get_width()/2),_Height+20)
    SURFACE.blit(health_bar_case, pos)
    SURFACE.blit(health_bar, pos, (0, 0, health_bar.get_width()*(_Health/_MaxHealth), health_bar.get_height()))

def DrawBattleButton(_text, _pos_x, _pos_y, _color):
    pg.draw.rect(SURFACE, BACKGROUND_COLOR, (_pos_x - BATTLE_BUTTON['size_x']/2, _pos_y - BATTLE_BUTTON['size_y']/2 , BATTLE_BUTTON['size_x'], BATTLE_BUTTON['size_y']))
    pg.draw.rect(SURFACE, _color, (_pos_x - BATTLE_BUTTON['size_x']/2, _pos_y - BATTLE_BUTTON['size_y']/2 , BATTLE_BUTTON['size_x'], BATTLE_BUTTON['size_y']), 5)
    _dialog = system_font_medium.render(_text, True, _color)#머여 갑자기 맛이 갔ㄴ는디 스피커가
    SURFACE.blit(_dialog, (_pos_x - _dialog.get_width()/2, _pos_y - _dialog.get_height()/2))

def DrawBattleButtons(_highlight_btn_num):
    _pos_x = WIDTH/5*2/4*1
    _pos_y = HEIGHT/8*1
    if(_highlight_btn_num==1):
        DrawBattleButton(BATTLE_BTN_1, _pos_x, _pos_y, HIGHLIGHT_COLOR)
    else:
        DrawBattleButton(BATTLE_BTN_1, _pos_x, _pos_y, BUTTON_COLOR)
    
    _pos_x = WIDTH/5*2/4*3
    _pos_y = HEIGHT/8*1
    if(_highlight_btn_num==2):
        DrawBattleButton(BATTLE_BTN_2, _pos_x, _pos_y, HIGHLIGHT_COLOR)
    else:
        DrawBattleButton(BATTLE_BTN_2, _pos_x, _pos_y, BUTTON_COLOR)

    _pos_x = WIDTH/5*2/4*1
    _pos_y = HEIGHT/8*2
    if(_highlight_btn_num==3):
        DrawBattleButton(BATTLE_BTN_3, _pos_x, _pos_y, HIGHLIGHT_COLOR)
    else:
        DrawBattleButton(BATTLE_BTN_3, _pos_x, _pos_y, BUTTON_COLOR)

    _pos_x = WIDTH/5*2/4*3
    _pos_y = HEIGHT/8*2
    if(_highlight_btn_num==4):
        DrawBattleButton(BATTLE_BTN_4, _pos_x, _pos_y, HIGHLIGHT_COLOR)
    else:
        DrawBattleButton(BATTLE_BTN_4, _pos_x, _pos_y, BUTTON_COLOR)

def DrawSkillsList(_pos_x, _pos_y, _size_x, _size_y):
    _count_size_y = 0
    _count_size_x = 0
    _sorted_keys = sorted(player.skills.keys())
    for _num in _sorted_keys:
        _skill = player.skills[_num]
        _skill_surface = system_font_small.render(f"{_num}. {_skill.name}", True, WHITE)
        _count_size_y += _skill_surface.get_height()*1.5
        SURFACE.blit(_skill_surface, (_pos_x, _pos_y + _count_size_y))

        if(_count_size_y >= _size_y- _skill_surface.get_height()):
            _count_size_y = 0
            _count_size_x += 0# NEEDFIX
        
def DrawItemsList(_pos_x, _pos_y, _size_x, _size_y):
    _count_size_y = 0
    _count_size_x = 0
    for i in range(len(item_list)):
        _item = item_list[i]['item']
        _item_surface = system_font_small.render(f"{i+1}. {_item.name}", True, WHITE)
        _count_size_y += _item_surface.get_height()*1.5
        SURFACE.blit(_item_surface, (_pos_x, _pos_y + _count_size_y))

        if(_count_size_y >= _size_y- _item_surface.get_height()):
            _count_size_y = 0
            _count_size_x += 0# NEEDFIX

def UseItem(_item_c):
    global player
    _item = _item_c['item']
    _is_used = False
    if(getattr(_item, 'itemType', '') == 'Consumable'):
        if(getattr(_item, 'target', 'self') == 'self'):
            for i in _item.effects:
            
                if(i['name'] == 'heal'):
                    BattleLogPush('§l§4' + str(player.GetHeal(i['value'])) + ' 만큼 회복했습니다!')
                    _is_used = True

    if(_is_used):
        for i in range(len(player.items)):
            if(player.items[i]['item'].id == _item.id):
                player.items[i]['amount'] -= 1
                if(player.items[i]['amount'] <= 0):
                    del player.items[i]
                break

def DrawPlayerState():
    _health_surface = info_font_medium.render(f'HP : {player.health}/{player.maxHealth}', True, WHITE)
    SURFACE.blit(_health_surface, (WIDTH/5*1 - _health_surface.get_width()/2, HEIGHT-_health_surface.get_height()))
def P_BattleDraw():
    '''
    general_control_state
    0 : 버튼 선택 (공격-아이템-관찰-도망)
    1 : 스킬 선택
    2 : 공격 중(적 피격 모션 + 마법 이펙트)
    3 : 적이 공격하는 중
    9 : 공격 중
    '''

    GameBorder()

    
    global is_enemy_hit
    global enemy_hit_count
    global general_control_state
    global is_input_end
    global is_input_start
    global input_number_length
    _highlight_btn_num = 0
    global highlight_btn_num_for_sfx
    global skill
    global is_input_backspace
    
    #Right--------------------------
    #enemyDraw
    if(is_enemy_hit):
        enemy_hit_count = tick_counter
        is_enemy_hit = False
    enemy.rect.center = EnemyPosition()#아 어차피 중심좌표구나 얜 어제 저녁엔 분명 괜찮았지 않나 왜이러지 enemy에 왜 []가 할당되는걸까
    
    
    all_sprites.update()
    all_sprites.draw(SURFACE)


    message_enemy_name = enemy_name_font.render(enemy.name, True, WHITE)
    SURFACE.blit(message_enemy_name, (WIDTH//5*2+(WIDTH//5*3)/2-(message_enemy_name.get_size()[0])/2, 15))  # 화면상에 제목 표시

    BgmCall(enemy.bgm)
    DrawEnemyCooltimeBar(enemy.maxCooltime, enemy.attackCooltime, message_enemy_name.get_height())
    BattleControl()
    

    DrawEnemyHealthBar(enemy.health, enemy.maxHealth, message_enemy_name.get_height())    
    #DrawTextBox()
    DrawBattleLog(1)

    #1. 싸움기술 2. 마법기술 3. 아이템 4. 도망
    if(general_control_state == 0):
        is_input_start = True
        input_number_length = 1
        #하이라이트
        if(input_number_str != '' and 1<=int(input_number_str)<=4):
            _highlight_btn_num = int(input_number_str)

        
        
        if(is_input_end and event.isBattle):
            if(input_number == 1):
                general_control_state = 1
                is_input_end = False
            if(input_number == 2):
                BattleLogPush(enemy.description)
                is_input_end = False
            if(input_number == 3):
                ItemListGet('name', 'Consumable')
                general_control_state = 3
                is_input_end = False
            if(input_number == 4):
                player.run = True
                is_input_end = False
        
        if(_highlight_btn_num != highlight_btn_num_for_sfx):
            highlight_btn_num_for_sfx = _highlight_btn_num
            SoundCall('change_select')
        DrawBattleButtons(_highlight_btn_num)

    if(general_control_state != 9 and is_input_backspace):
        if(input_number_str == ''):
            general_control_state = 0
        is_input_backspace = False
        

    if(general_control_state == 1):
        #왼쪽에 스킬 목록 띄우기
        is_input_start = True
        input_number_length = 2
        DrawSkillsList(UI_SKILL_BATTLE['pos_x'], UI_SKILL_BATTLE['pos_y'], UI_SKILL_BATTLE['size_x'], UI_SKILL_BATTLE['size_y'])
        if(is_input_end):
            is_input_end = False
            if(input_number in player.skills):
                skill = player.skills[input_number]
                skill.__init__()
                general_control_state = 9

    if(general_control_state == 3):
        is_input_start = True
        input_number_length = 2
        DrawItemsList(UI_SKILL_BATTLE['pos_x'], UI_SKILL_BATTLE['pos_y'], UI_SKILL_BATTLE['size_x'], UI_SKILL_BATTLE['size_y'])
        if(is_input_end):
            is_input_end = False
            if(len(item_list) >= input_number and input_number != 0):
                _item = item_list[input_number-1]
                UseItem(_item)
                general_control_state = 9


    if(general_control_state == 9):
        if(skill == None):
            general_control_state = 0
        
    #Left--------------------------
    #플레이어 스텟
    DrawPlayerState()
    #마법진
    DrawCircles(circle_arr, WIDTH/5, HEIGHT/5*4)
    DrawInputNumber(WIDTH/5, HEIGHT/5*4)
    





def BattleControl():
    global event
    global enemy
    global player
    global skill
    global is_input_end
    global is_input_start
    global input_number_length
    global event_stack
    #Battle Win or Defeat Checker
    #win
    if(enemy.health <= 0):
        if(event.isBattle):
            skill = None
            C_DelayClear('battle')
            BattleLogPush(f'§l§4{BATTLE_WIN_MSG}')
        event.isBattle = False
        if(C_Delay("BattleEnd", tick_counter, 2 * TICK_PER_SEC)):
            event.callEndFuntion()
            PageChange(ADVENTURE_PAGE_NUM)

    #defeat

    elif(player.health <= 0):
        if(event.isBattle):
            skill = None
            C_DelayClear('battle')
            BattleLogPush(f'{BATTLE_DEATH_MSG}')
        event.isBattle = False
        if(C_Delay("BattleEnd", tick_counter, 3 * TICK_PER_SEC)):
            event.__init__()
            event.reset()
            
            event_stack = []
            event_stack.append(E_Death())
            event_stack[0].DialogSet(event)
            player.health = player.maxHealth
            event_stack.append(event)
            PageChange(ADVENTURE_PAGE_NUM)#아 이게 숲으로 이동이 되네? 왜지
            event.End()

    #도망치기
    elif(player.run == True):
        if(not getattr(enemy, 'isEscapable', True)):
            _enemy_escape_msg = getattr(enemy, 'escapeMsg', '')
            BattleLogPush(f'{BATTLE_CANT_RUN_MSG} §3{_enemy_escape_msg}')
            player.run = False
        else:
            if(event.isBattle):
                skill = None
                C_DelayClear('battle')
                BattleLogPush(f'{BATTLE_ESCAPE_MSG}')
            event.isBattle = False
            if(C_Delay("BattleEnd", tick_counter, 3 * TICK_PER_SEC)):
                event.callEndFuntion()
                PageChange(ADVENTURE_PAGE_NUM)

    else:
        #Enemy
        enemy.attackCooltime -= player.timeScale_t
        if(enemy.isAttacking):
            BattleLogPush(f'§l§8{enemy.name}의 {enemy.skillName}! Damage {str(enemy.skillDamage)} ')
            if(hasattr(enemy, 'skillDialog')):
                BattleLogPush(f'§l§0{enemy.skillDialog}')
            PlayerHurt()
            enemy.isAttacking = False

        #Player
        player.UpdateBattle()
        if(skill != None):
            #수입력 및 체크
            is_input_start = True
            
            if(skill.formula != [] and skill.isAttacking and skill.success):
                input_number_length = len(skill.formula[0])+1
                DrawFormula(skill.formula[0][0])
                if(is_input_end):
                    is_input_end = False
                    if(input_number != skill.formula[0][1]):
                        skill.success = False
                    else:
                        del skill.formula[0]
                    if(skill.formula == [] and skill.skillCount == 1):
                        BattleLogPush(f'§l§0{skill.name}!')
                        if(getattr(skill, 'sfx', '') != ''):                        
                            SoundCall(skill.sfx, 2)
    
                    
                    
            elif(skill.isAttacking and skill.success):
                SkillControl()
                if(getattr(skill, 'sfx', '') != ''):
                    SoundCall(skill.sfx, 2)
                skill.isAttacking = False

            elif(skill.isAttacking and skill.success == False):
                print("패널티 부가") #NEED ADD : 문제 실패시 정신력 감소
                BattleLogPush(f'§l§3{BATTLE_SKILL_FAIL}')
                skill.isAttacking = False
                #실패

            
            if(skill.timeDelay <= 0):
                skill.OnSkill(player)
            else:
                skill.timeDelay -= 1

            if(skill.isEnd == True):
                skill = None

        enemy.Battle()

def PlayerHurt():
    global enemy
    global player
    #NEED FIX : 적 공격도 플레이어 무기처럼 damage 통합시키기
    #그리고 플레이어 방어스탯, 적 방어스탯 등등 resist, damage같은 모든 수치를 통합시키기
    if(enemy.skillType == 'damage'):
        if(enemy.skillDamageType == 'physical'):
            if(player.parryingTick <= 0): 
                player.GetDamage(enemy.skillDamage)
            else:
                player.parryingTick = 0
                BattleLogPush(f'{BATTLE_PARRYING_MSG}')

def SkillControl():
    global enemy
    global player
    global skill
    global enemy_hit_count

    if(skill.type == 'damage'):
        if(skill.target == 'enemy'):
            _damage = 0
            _damage_percent = -1
            _is_ciritical = False
            _critical_damage = 100
            #데미지 합산
            for _status, _value in skill.damageStatus.items():
                if(_status == 'damage'):
                    _damage += _value
                elif(_status == 'str'):
                    _damage += _value * player.str
                elif(_status == 'int'):
                    _damage += _value * player.int

                elif(_status == 'damage_r'):
                    _damage += _value * player.str
                elif(_status == 'str_r'):
                    _damage += _value * player.str
                elif(_status == 'int_r'):
                    _damage += _value * player.int
                elif(_status == 'random'):
                    _damage_percent = random.randrange(_value[0], _value[1])/100
            
            if(_damage_percent >= 0):
                _damage = int(_damage * _damage_percent)
            if(_is_ciritical):
                _damage = _damage * _critical_damage

            if(getattr(skill, 'damageType', 'physical') == 'physical'):
                _damage = _damage * (1 - enemy.resistPhysical)

            #데미지 단순화
            _damage = int(_damage)
                
            #enemy checking
            enemy.health -= _damage
            enemy_hit_count = tick_counter #NEED FIX : 전역변수 치우고 얘도 C_Delay로 처리하기
            if(_is_ciritical):
                BattleLogPush(f'§l§3 {BATTLE_CRITICAL_MSG}')
            if(hasattr(skill, 'dialog')):
                if(skill.dialog != []):
                    BattleLogPush('§l§3' + random.choices(skill.dialog)[0] + f' §3{str(_damage)} {BATTLE_ATTACK_MSG}')
            else:
                BattleLogPush(f'§l§3{str(_damage)} {BATTLE_ATTACK_MSG}')
    elif(skill.type == 'buff'):
        if(getattr(skill, 'target', 'self') == 'self'):
            for i in skill.effects:
                _effect = i
                if(_effect['name'] == 'parrying'):
                    player.parryingTick = _effect['tick'] #대충 개발은 여까지 하고 발표자료나 만들자
                elif(_effect['name'] == 'blocking'):
                    player.blockingTick = _effect['tick']

        if(hasattr(skill, 'dialog')):
            print(player.blockingTick, player.parryingTick)
            if(skill.dialog != []):
                BattleLogPush('§l§3' + random.choices(skill.dialog)[0])




#NEED FIX : 현재 Physical이나 Damage... 그러니까 미흡함 -> 공격 처리 시스템 제대로 구축(저항 고려)
def BattleAttackEnemy(_type, _damage, **_key):# attackType, attackDamage, other. ex) "Fire", 20, duration=5, dotDamage=1...
    global enemy 
    if(_type == 'normal'):
        enemy.health -= _damage * (1- enemy.resistPhysical)
        
#랜덤 수식 생성기~~~...를 만들 차례

def EnemyPosition(): #for EnemyHitted
    _enemy_pos_x = WIDTH//5*2+(WIDTH//5*3)/2
    _enemy_pos_y = HEIGHT/2
    if(enemy_hit_count < tick_counter - TICK_PER_SEC * 0.4):
        _enemy_pos = (_enemy_pos_x+20, _enemy_pos_y)

    elif(enemy_hit_count < tick_counter - TICK_PER_SEC * 0.3):
        _enemy_pos = (_enemy_pos_x-20, _enemy_pos_y)

    elif(enemy_hit_count < tick_counter - TICK_PER_SEC * 0.2):
        _enemy_pos = (_enemy_pos_x+20, _enemy_pos_y)

    elif(enemy_hit_count < tick_counter - TICK_PER_SEC * 0.1):
        _enemy_pos = (_enemy_pos_x-20, _enemy_pos_y)

    else:
        _enemy_pos = (_enemy_pos_x, _enemy_pos_y)

    return _enemy_pos

def EventEffectApply(_event = ''):
    global enemy
    global event_stack
    global event
    global all_sprites
    if(_event == ''):
        _event_effect = event.effects
    for i in _event_effect:
        if(i['name'] == 'battle'):
            _enemies = [],[]
            for p in i['enemies']:
                _enemies[0].append(p['enemy'])
                _enemies[1].append(p['chance'])
            enemy = random.choices(_enemies[0],_enemies[1])[0](pg)
            
            all_sprites = pg.sprite.Group()
            all_sprites.add(enemy)
            
            enemy.__init__(pg) #아 잠깐 이거 이벤트가 아니라 엥?아니 맞는데
        if(i['name'] == 'modifyState'):
            setattr(player, i['value'], getattr(player, i['value'], 0) + i['amount'])

        if(i['name'] == 'appendEvent'):
            event_stack.append(i['value']())

        
        if(i['name'] == 'setWorldValue'):
            player.SetWorldValue(i['key'], i['data'])

    event.isEventCheck = False
            

#NEED FIX : 랜덤 이벤트 큐를 없애고, 이벤트 내에서 독자적으로 랜덤 이벤트 제공하기. 만약 이벤트가 비어있을 시 기다리도록 수정하기
#그리고 빠르게 페이지 전환시 페이지 초기화되는 오류 = 위에 본것처럼 event_stack에 다음 이벤트가 추가되기도 전에 이벤트가 시작되어서 그럼
#또또또한 프레임 2~3씩 손실나는거 찾기
def EventRandomModify(_event, _percent = 0, _is_fix = False):
    if(_percent == 0):
        _percent = _event.percent
    if(_event not in event_randoms):
        event_randoms[0].append(_event)
        event_randoms[1].append(_percent)
    else:
        if(_is_fix):
            _pos = event_randoms[0].index(_event)
            event_randoms[1][_pos] = _percent
        else:
            _pos = event_randoms[0].index(_event)
            event_randoms[1][_pos] += _percent

    
def EventRandomChoose():
    _event = random.choices(event_randoms[0],event_randoms[1])[0]

    return _event

def NeedsCheck(_needs_father):
    _is_pass = True
    for _need in _needs_father['needs']:
        if(_need['name'] == "haveTool"):
            if(_need['value'] not in player.items):
                _is_pass = False

        elif(_need['name'] == "cellUp"):
            if(event.cells.index(event.nowCell) < _need['value']):
                _is_pass = False


        elif(_need['name'] == "cellDown"):
            if(event.cells.index(event.nowCell) > _need['value']):
                _is_pass = False

        elif(_need['name'] == "getWorldValue"):
            if(player.GetWorldValue(_need['key']) != _need['data']):
                _is_pass = False

    return _is_pass 

def DrawEventSelect(_selects):
    global is_input_start
    global input_number_length
    global is_input_all
    global is_input_num_minus
    is_input_num_minus = False
    is_input_start = True
    is_input_all = True
    input_number_length = 1


    _selections_count = len(_selects)

    
    #dialogSize 만약 사이즈가 안 맞을 경우
    _temp_dialog = dialog_font.render('M', True, WHITE)
    _char_width, _char_height = _temp_dialog.get_size()
    _text_space = _selections_count * (_char_height+6)
    pg.draw.rect(SURFACE, BLACK, (WIDTH/5*2, HEIGHT-_text_space, WIDTH/5*3, _text_space))
    _pos_x = WIDTH/5*2 + _char_width * 1
    _pos_y = HEIGHT-_text_space
    _line_scale = 1
    for i in range(_selections_count):
        if(input_number_str == str(i+1) and general_control_state != 1):
            pg.draw.rect(SURFACE, ORANGE, (WIDTH/5*2, _pos_y+_line_scale, WIDTH/5*3, _char_height+6))
        _event_dialog = str(i+1)+'. '+_selects[i]['text']
        if(NeedsCheck(_selects[i])):
            _event_text = dialog_font.render(_event_dialog, True, WHITE)
        else:
            _event_text = dialog_font.render(_event_dialog, True, GRAY)

        
        _pos_y += 3
        SURFACE.blit(_event_text, (_pos_x, _pos_y))
        _pos_y += _char_height + 3
        pg.draw.line(SURFACE, WHITE, (WIDTH/5*2, _pos_y), (WIDTH, _pos_y), _line_scale)

    pg.draw.line(SURFACE, WHITE, (WIDTH/5*2, HEIGHT-_text_space), (WIDTH, HEIGHT-_text_space), 1)




def DrawEventText(_start_time, _speed):
    '''
    _start_time : 말을 시작한 tick
    _text : 말할 내용 str
    _speed : 말하는 속도
    ... return : 대사 끝나는 tick_counter값 반환
    '''
    global is_input_wheel
    global input_wheel
    is_input_wheel = True

    _speed *= DIALOG_SPEED
    _dialog = event.dialog
    
    for i in event.prefixDialog:
        if(NeedsCheck(i)):
            _dialog += i['text']
        elif(i['else'] != ''):
            _dialog += i['else']

    for i in event.suffixDialog:
        if(NeedsCheck(i)):
            _dialog = i['text'] + _dialog
        elif(i['else']!= ''):
            _dialog = i['else'] + _dialog 

    _char_width, _char_height = dialog_font.size('M')
    _pos_x = WIDTH/5*2
    _pos_x_center = WIDTH/5*3.5 #머지... 뭔가...
    _pos_y = _char_height + UI_ADVENTURE_TOP_BAR['size_y'] + UI_ADVENTURE_TOP_BAR['pos_y']
    _size_x = WIDTH/5*3-_char_width*1
    #왜 가운데 정렬만 그렇지
    _enter_count =  _dialog.count('\n')
    _text_length = len(_dialog) - _dialog.count('\n') - _dialog.count('§')*2

    #EnterCounter Calculate 
    #아ㅋㅋㅋㅋㅋㅋ그거로 하자
    #수학 문제가 있는데 일반 공격도 마법 공격도 다 수학에 의존하자
    # str, int는 데미지 자체에 관여하고 dex, wis는 난이도에 관여하는거야 쉬울수록 빨리 풀 거 아냐 이거다 그러면 다 가능이지

    _text_time_length = _text_length * TICK_PER_SEC / _speed
    _char_time_length = TICK_PER_SEC / _speed
    _current_time = tick_counter - _start_time#진행된 시간
    _now_text_point = int(_current_time//_char_time_length)
    _output_text = _dialog[:]
    
    _count = 0
    #NEED FIX : event 각 크기랑 글자 크기 따져서 글 다 내리면 더이상 안내려지게
    #NEED FIX : select라던가 그런 인수들을 매 프레임마다 불러오는 대신 인벤토리처럼 한 번 불러와서 다시쓰기 -> 그래야 가공하는데에 성능낭비 덜 될듯
    if(input_wheel > 3):
        input_wheel = 3
    
    if(input_wheel < -(_enter_count - 5) and input_wheel > 3):
        input_wheel = -(_enter_count - 5)
    
    _pos_y = _pos_y - (_char_height+5) * -(input_wheel+DIALOG_POS_Y)

    #
    while(_now_text_point>0 and _output_text != ''):
        _point = 0
        _text_arr = []
        _is_center = False
        _text_width = 0 #배치용 width

        _now_text_size = 0 #슬라이스용 width

        _temp_i = 0
        _previous_color = 0
        _previous_state = 'l'
        while(_temp_i < len(_output_text)):
            i = _output_text[_point]
            if(i == '§'):
                _now_text_point += 1 
                if(_output_text[_point + 1] in DIALOG_COLORS):
                    _previous_color = _output_text[_point + 1]
                else:
                    _previous_state = _output_text[_point + 1]
            else:
                _now_text_point -= 1

                if(re.sub('[^가-힣]', '', i) != ''):
                    _now_text_size += _char_width * 2
                else:
                    _now_text_size += _char_width


            if(_now_text_size >= _size_x):
                _text_arr.append(_output_text[:_point-1])
                _output_text = f"\n§{_previous_state}§{_previous_color}" + _output_text[_point-1:]
                _now_text_point += 2
                break

            if(0 >= _now_text_point):
                _text_arr.append(_output_text[:_point])
                _output_text = _output_text[_point:]
                break

            if(i == '\n'):
                _text_arr.append(_output_text[:_point])
                _output_text = _output_text[_point:]
                break

            
            _point +=1
            _temp_i += 1

        
        if(_text_arr != []):
            _text_arr = _text_arr[0].split('§')

        


        #NEED ADD : 글자 색이 실시간으로 바뀌게 마법진이랑 메인화면 oppacity 코드 참조해서
        if(len(_text_arr)>1):
            _line_type = _text_arr[1]
            if(_line_type == 'c'):
                _is_center = True
                del _text_arr[0]
                del _text_arr[0]
            if(_line_type == 'l'):
                _is_center = False
                del _text_arr[0]
                del _text_arr[0]


        #횡 사이즈 계산
        for i in _text_arr:
            _text_width += (len(i)-1) * _char_width
            _text_width += (len(re.sub('[^가-힣]', '', i))) * _char_width

        _last_text_width = 0

        for _word in _text_arr:
            if(_word != [] and _word != ''):
                if(_word[0] in DIALOG_COLORS):
                    _word_color = DIALOG_COLORS[_word[0]]
                    _word = _word[1:]
                else:
                    _word_color = DIALOG_COLORS['0']
                
            

            _text_surface = dialog_font.render(_word, True, _word_color)

            if(_is_center):
                _text_pos = (_pos_x_center-(_text_width/2)+_last_text_width-_char_width, _pos_y - _text_surface.get_height()/2 +_count*(_char_height + 5))
            else:
                _text_pos = (_pos_x + _char_width + _last_text_width, _pos_y - _text_surface.get_height()/2 +_count*(_char_height + 5))
                
            _last_text_width += _text_surface.get_width()
            SURFACE.blit(_text_surface, _text_pos)



            #후처리
        if(_output_text != ''):
            if(_output_text[0] == '\n'):
                _output_text = _output_text[1:]
                _count += 1
                _is_center = False
                    

    

    _end_time = _start_time + _text_time_length
    
    return _end_time
#아 아이템 리스트는 계속 받아오고 sort도 계속 처리하면 진짜 이건 무조건 성능이슈 뜬다. 이건 따로 독립시키자
def ItemListGet(_sort_key = 'name', _filter_key = 'All'):
    global item_list
    item_list = player.items.copy()
    ItemListSort(_sort_key, _filter_key)

def ItemListSort(_sort_key = 'name', _filter_key = 'All'):
    global item_list
    if(_filter_key != 'All'):
        item_list = filter((lambda x: getattr(x['item'], 'itemType', '') == _filter_key), item_list)
    
    

    #NEED FIX : sort key...이건 일일히 하나하나 해야할 듯 이름, 갯수, 이런게 다 다른 부분에 있음
    item_list = sorted(item_list, key = lambda x: getattr(x['item'], _sort_key))

def DrawInfoItems():
    global input_number_str
    global info_scroll_count
    global is_input_end
    _count_size_y = 0
    _count_size_x = 0 #아 깊은복사 얕은복사는 원조가 바뀌는건 따라가는거고 짭이 바뀌면 독립되는거였구나 난 짭 바뀌면 원조도 바뀌는건줄
    #인벤토리를 어떻게 할까 스크롤할까 아니면 넘버키를 좀 바꿔서 8위 2밑 이런 느낌으로... 스읍 아 근데
    #그렇게 하면 위에 있는 숫자로는 하기 힘들겠구나 1 2 3 4 5 6 7 8 9 로 해서 3개씩 띄우기로 하자 #아!!!!!!카타클리즘!!!!!!!
    #그래 그냥 카타클리즘처럼 기본 베이스는 숫자입력으로 하되 추가로 화살표를 쓸 수 있게 하면 그만이잖아~~~난 천잰가???(모방의)
    #어제 자다가 생각났는데 약간 위아래 돌리는 것처럼 밑에 9누르면 밑에꺼가 올라오는 그런 느낌이면 아 어차피 arrow 쓸꺼지어 ?
    #아 넘버패드 그거 안되네 ㅎ...

    #_arr 처리
    _small_font = info_font_small
    _font = info_font_medium
    _big_font = info_font_medium
    _items_arr = item_list

    _char_width, _char_height = _font.size('M')
    
    '''
    쫘라락 번호가 매겨지고....
    '''



    #Input str check
    if(input_number_str == '1' and info_scroll_count != 0):
        info_scroll_count -= 1
        input_number_str = '2'
    if(input_number_str != ''):
        if(int(input_number_str) >= 10):
            input_number_str = '9'
        if(int(input_number_str) <= 0):
            input_number_str = '1'

    if(input_number_str == '9' and info_scroll_count != len(_items_arr)-9):
        info_scroll_count += 1
        
        input_number_str = '8'
    
    


    
    #최소 제한
    if(info_scroll_count < 0 or len(_items_arr) <= 9):
        info_scroll_count = 0
    

    #최대 제한
    if(len(_items_arr)>=9):
        if(info_scroll_count > len(_items_arr)-9 and info_scroll_count > 9):
            info_scroll_count = len(_items_arr)-9 
    else:
        if(input_number_str != ''):
            if(int(input_number_str)> len(_items_arr)):
                input_number_str = str(len(_items_arr))

    _pos_x = UI_INFO_WINDOW['pos_x'] - UI_INFO_WINDOW['size_x']/2
    _pos_y = UI_INFO_WINDOW['pos_y']-UI_INFO_WINDOW['size_y']/2

    #LEFT################################################################
    _pos_vertical = UI_INFO_WINDOW['size_x']/3*2
    #Top Bar Draw
    pg.draw.line(SURFACE, DEEP_GRAY, (_pos_x, _pos_y + _char_height * 2), (_pos_x + _pos_vertical, _pos_y + _char_height * 2), 1)
    pg.draw.line(SURFACE, WHITE, (_pos_x + _pos_vertical, _pos_y), (_pos_x + _pos_vertical, _pos_y + UI_INFO_WINDOW['size_y']), 5)

    #NEED ADD : 무기 필터 켜져있을 경우 공격력 표시

    _pos_y += _char_height * 0.5

    #title draw    
    _top_bar_surface = _font.render("이름", True, WHITE)
    SURFACE.blit(_top_bar_surface, (_pos_x - _top_bar_surface.get_width()/2+ _pos_vertical/5*1.5, _pos_y))
    
    _top_bar_surface = _font.render("수량", True, WHITE)
    SURFACE.blit(_top_bar_surface, (_pos_x - _top_bar_surface.get_width()/2 + _pos_vertical/5*3.5, _pos_y))
    
    _top_bar_surface = _font.render("종류", True, WHITE)
    SURFACE.blit(_top_bar_surface, (_pos_x - _top_bar_surface.get_width()/2 + _pos_vertical/5*4.5, _pos_y))
    
    _pos_y += _char_height * 1.5 

    #line draw NEED FIX : 윤곽선 침범
    pg.draw.line(SURFACE, DEEP_GRAY, (_pos_x + _pos_vertical/5*4 , _pos_y), (_pos_x + _pos_vertical/5*4, _pos_y - _char_height * 2 + UI_INFO_WINDOW['size_y']), 1)
    pg.draw.line(SURFACE, DEEP_GRAY, (_pos_x + _pos_vertical/5*3 , _pos_y), (_pos_x + _pos_vertical/5*3, _pos_y - _char_height * 2 + UI_INFO_WINDOW['size_y']), 1)



    for i in range(0, 9):
        _pos_x_t = _pos_x
        _pos_x_t += _char_width * 1.5
        _pos_y += 5
        if(i + info_scroll_count >= len(_items_arr)):
            break
        _now_item = _items_arr[i + info_scroll_count]
        #+ _item_name_surface.get_width()/2
        #highlight
        _text_color = WHITE
        if(input_number_str == str(i + 1)):
            _text_color = ORANGE
        _item_name_surface = _font.render(f"{i + 1}. {getattr(_now_item['item'], 'name', '손상된 아이템')}", True, _text_color)
        SURFACE.blit(_item_name_surface, (_pos_x_t , _pos_y))
        _pos_y += _char_height

        
        
    #RIGHT################################################################
    _pos_y = UI_INFO_WINDOW['pos_y']-UI_INFO_WINDOW['size_y']/2
    _pos_y += _char_height * 0.5
    _right_size = UI_INFO_WINDOW['size_x'] - _pos_vertical
    if(input_number_str != ''):
        if(info_scroll_count + int(input_number_str) - 1 < len(_items_arr)):
            _now_item = _items_arr[info_scroll_count + int(input_number_str) - 1]
        else:
            _now_item = _items_arr[len(_items_arr) - 1]
        #Item Name
    
    _item_info_title = _big_font.render(f"{getattr(_now_item['item'], 'name', '손상된 아이템')}", True, WHITE)
    SURFACE.blit(_item_info_title, (_pos_x + _pos_vertical + _right_size/2 - _item_info_title.get_width()/2, _pos_y))
    
    _pos_y += _char_height * 1.5
    #Item Description
    _item_info_desc = _small_font.render(f"{getattr(_now_item['item'], 'description', '...')}", True, WHITE)
    SURFACE.blit(_item_info_desc, (_pos_x + _pos_vertical + _right_size/2 - _item_info_desc.get_width()/2, _pos_y))
    

#나중에 화면 크기에 따라 폰트 조절 꼭 필요할듯...
    #TRIGGER
    if(is_input_end):
        #아이템 사용 처리
        is_input_end = False


def DrawInfoWindow():
    '''
    인벤토리, 상태창 그외 잡다한 거 띄우기
    '''
    _menus = INFO_MENUS
    _char_width, _char_height = info_font_large.size('M')
    
    _string_width = info_font_large.render(_menus[0], True, WHITE).get_width()

    if(info_window_state >= 0):
        _box_height = _char_height * (len(_menus)+2)
        _box_width = _string_width + _char_width * 2
        _box_pos_x = UI_INFO_WINDOW['pos_x'] - UI_INFO_WINDOW['size_x']/2 - _box_width/2 - _box_width/2

        #좌측 메뉴 박스 띄우기
        pg.draw.rect(SURFACE, BLACK, (_box_pos_x, UI_INFO_WINDOW['pos_y']-UI_INFO_WINDOW['size_y']/2, _box_width, _box_height))
        pg.draw.rect(SURFACE, WHITE, (_box_pos_x, UI_INFO_WINDOW['pos_y']-UI_INFO_WINDOW['size_y']/2, _box_width, _box_height), 5)
        

        #메뉴 안에 글쓰기 및 하이라이트 해주기
        for i in range(len(_menus)):
            if(input_number_str == str(i+1) and info_window_state == 0):
                _menu = info_font_large.render(_menus[i], True, ORANGE)
            else:
                _menu = info_font_large.render(_menus[i], True, WHITE)
            SURFACE.blit(_menu, (_box_pos_x + _char_width, UI_INFO_WINDOW['pos_y'] - UI_INFO_WINDOW['size_y']/2 + _box_height / len(_menus) * i + _char_height/4))

        #중앙 메뉴 박스 띄우기
        if(info_window_state >= 1):
            pg.draw.rect(SURFACE, BLACK, (UI_INFO_WINDOW['pos_x'] - UI_INFO_WINDOW['size_x']/2, UI_INFO_WINDOW['pos_y']-UI_INFO_WINDOW['size_y']/2, UI_INFO_WINDOW['size_x'], UI_INFO_WINDOW['size_y']))#크 이거지
            pg.draw.rect(SURFACE, WHITE, (UI_INFO_WINDOW['pos_x'] - UI_INFO_WINDOW['size_x']/2, UI_INFO_WINDOW['pos_y']-UI_INFO_WINDOW['size_y']/2, UI_INFO_WINDOW['size_x'], UI_INFO_WINDOW['size_y']), 5)
            #if(info_window_state == 1):
                #pg.draw.rect(SURFACE, WHITE, ())
        
        #
        if(info_window_state == 1): #여기선... 어떤 코드를 갖다 쓰지
            DrawInfoItems()
            
            #아이템 목록 보여주기

            #pg.draw.rect(SURFACE, BLACK, (UI_INFO_WINDOW['pos_x'], UI_INFO_WINDOW['pos_y'], UI_INFO_WINDOW['size_x'], UI_INFO_WINDOW['size_y']))
    #밥 먹어야지



def DrawAdventureTopBar():
    pg.draw.rect(SURFACE, BLACK, (UI_ADVENTURE_TOP_BAR['pos_x'], UI_ADVENTURE_TOP_BAR['pos_y'], UI_ADVENTURE_TOP_BAR['size_x'], UI_ADVENTURE_TOP_BAR['size_y']))
    pg.draw.line(SURFACE, WHITE, (UI_ADVENTURE_TOP_BAR['pos_x'], UI_ADVENTURE_TOP_BAR['size_y']), (UI_ADVENTURE_TOP_BAR['pos_x'] + UI_ADVENTURE_TOP_BAR['size_x'], UI_ADVENTURE_TOP_BAR['size_y']))
    
    
    if(event.nowCell != ''):
        _state_text = system_font_medium.render(f" HP:{player.health}/{player.maxHealth} {event.region}-{event.area}-{event.nowCell} ", True, WHITE)
    else:
        _state_text = system_font_medium.render(f" HP:{player.health}/{player.maxHealth} {event.region}-{event.area} ", True, WHITE)
    SURFACE.blit(_state_text, (UI_ADVENTURE_TOP_BAR['pos_x'], UI_ADVENTURE_TOP_BAR['pos_y']+ UI_ADVENTURE_TOP_BAR['size_y']/2 - _state_text.get_height()/2))
    #두번째, 시간 밥좀 먹고옴
    #세번째, 

def P_AdventureDraw():
    '''
    general_control_state
    0 : normal
    1 : openInventory
    '''
    global event_tick 
    global is_any_key_pressed
    global is_input_start
    global is_input_end
    global input_wheel
    global event
    global battle_log
    global general_control_state
    global info_window_state
    global input_number_str
    global is_input_all
    global info_scroll_count
    global is_input_backspace
    global last_event

    
    #BGM
    #BgmCall('AdventureMenu', 0.6)
    
    
    is_input_start = True
    is_input_all = True
    #Skip
    #selects 처리
    _selects = []
    for i in event.selections:
        if(NeedsCheck(i)):
            _selects.append(i)
        else:
            if(not getattr(i, 'hide', True)):
                _selects.append(i)


    GameBorder()
    
    #대사 출력  *위치 밑으로 내리지 말 것
    if(DrawEventText(event_tick, 1) < tick_counter):
        DrawEventSelect(_selects)


    #키 입력 관리
    if(is_any_key_pressed):
        event_tick -= 100
        if(input_number_str == '0' or input_number_str == '-0'):
            if(general_control_state == 0):
                general_control_state = 1
            elif(general_control_state == 1):
                general_control_state = 0
            info_window_state = 0
            input_number_str = ''
        is_any_key_pressed = False

    BgmCall(event.bgm, 1)
    DrawCircles(circle_arr, WIDTH/5)
    DrawInputNumber(WIDTH/5, HEIGHT/5*4)


    if(general_control_state == 0):
        #키입력
        if(is_input_end):
            #인벤창 열기
            #선택지 선택
            if(input_number <= len(_selects)):
                
                if(NeedsCheck(_selects[input_number-1])):
                    _selects[input_number-1]['function']()
                    input_wheel = 0
                    event_tick = tick_counter
            is_input_end = False

    elif(general_control_state == 1): 
        if(is_input_end):
            input_number_str = '1'
            is_input_backspace = False
            if(input_number <= len(INFO_MENUS) and info_window_state == 0):
                info_scroll_count = 0
                info_window_state = input_number #인벤토리용으로 따로 키 입력을 만들어야겠다... 진짜 세상 비효율적이네 일단 오늘은 여기까지
                #인벤토리 오픈시
                if(info_window_state == 1):
                    ItemListGet()
                #info_window_state > 0일시 is_input_end는 내부에서 처리
                is_input_end = False
                
        if(is_input_backspace):
            if(info_window_state == 0):
                general_control_state = 0
            elif(info_window_state >= 0):
                info_window_state = 0
            is_input_backspace = False
        DrawInfoWindow()
        
        
    #Show Event Selections
    

    if(event.isEventCheck):
        EventEffectApply()
        event_tick = tick_counter
        event.isEventCheck = False

    #BattleCheck
    if(event.isBattle and not event.isEventCheck):
        #Battle Log Clear
        for i in range(len(battle_log)):
            battle_log[i] = ''

        enemy.__init__(pg)
        skill.__init__()
        PageChange(BATTLE_PAGE_NUM)
        




    #LEFT


    





    #RIGHT
    #입력 자...이벤트를 어떻게 컨트롤할까..
    DrawAdventureTopBar()


    


    #END
    if(event.isEnd):
        #이펙트 검사 마지막으로 함 더 아니 이게 왜 event를 집어 넣어줘야하는거지? 어? 잠깐 이러면 그럴 일이 없는데 해결!! EventEffectApply()를 중복 실행해서 그랬음
        if(event.isEventCheck):
            EventEffectApply()

        #이벤트 선택
        last_event = None
        event.isEnd = False
        last_event = event
        
        if(event_stack != []):
            event = event_stack.pop(0)
        else: #아 이벤트 스택에 두번 들어가지는구나!!!!!!!!!!!!
            event = EventRandomChoose()
        event.__init__()
        if(hasattr(event, 'ComeInCheck')):
            event.ComeInCheck(last_event)


        #만약 이후 이벤트 예정이 있다면? 예정 이벤트 진행
        #없다면? 랜덤 이벤트 선택
        #그리고 이 랜덤 이벤트들도 목록 해줘야지
    


def P_MainmenuDraw():
    global is_any_key_pressed
    global any_key_pressed_tick
    global general_control_state
    global circle_arr
    global is_input_start
    global is_input_end
    global input_number_length
    global highlight_btn_num_for_sfx
    global is_input_all
    global tick_counter
    '''
    0 : wait for press any key.
    1 : 메인 화면 올라가는 중, 
    2 : 메뉴들 띄워줌
    '''
    #Title
    _title_text = pg.image.load(MAIN_TITLE_IMAGE_PATH)
    _title_text = pg.transform.scale(_title_text, (_title_text.get_width()*2, _title_text.get_height()*2))

    BgmCall('MainMenu')
    #CirclePosition
    _circle_position_x = WIDTH/2
    _circle_position_y = HEIGHT/5*3
    
    _pre_select = 0
    #NEED FIX : 키입력 개선 -> global is_any_key_pressed로 해결
    #STATE 0 please press any button  
    if(is_any_key_pressed and general_control_state == 0 and next_page_state == now_page_state):
        general_control_state = 1
        SoundCall('press_start')
        is_any_key_pressed = False
        any_key_pressed_tick = tick_counter

    #STATE 1
    if(general_control_state >= 1):
        #NEED FIX : y좌표 천천히 이동
        _title_pos_y = ()#근데... 이걸 그럼 하려면 아..어... 이게 그 y좌표가 또 저장할려면 global값 써야하잖아... 이게 맞나...이럴꺼면... 이런 자잘한 건 나중으로 좀 미뤄두자
        if(HEIGHT/2 - _title_text.get_height()/2  -  ((tick_counter-any_key_pressed_tick)*3)> HEIGHT/5 - _title_text.get_height()/2 and general_control_state == 1):
            _title_pos = (WIDTH/2 - _title_text.get_width()/2, HEIGHT/2 - _title_text.get_height()/2  -  ((tick_counter-any_key_pressed_tick)*3) )
            if(is_any_key_pressed):
                tick_counter += 1000
        else:
            _title_pos = (WIDTH/2 - _title_text.get_width()/2, HEIGHT/5 - _title_text.get_height()/2)
            if(general_control_state == 1):
                circle_arr = [[0, 0, 0, 5, 'normal_white', 1],
                        [0, 0, 0, 10, 'normal_red', 0.9],
                        [0, 0, 0, -10, 'normal_white', 1.1],
                        #[WIDTH/5, HEIGHT/2, 0, -1, 'normal_red_square', 1.1],
                        ]
                general_control_state = 2
                input_number_length = 1
                is_input_all = True
    else:
        #print: Press any Button and Title
        _press_any_key_bliking_speed = 3
        _title_pos = (WIDTH/2 - _title_text.get_width()/2, HEIGHT/2 - _title_text.get_height()/2)
        _press_any_key = dialog_font.render(PRESS_ANY_KEY, True, WHITE)
        if(((tick_counter*_press_any_key_bliking_speed)//255)%2 == 0):
            _press_any_key.set_alpha((tick_counter*_press_any_key_bliking_speed)%255)
        else:
            _press_any_key.set_alpha(255-(tick_counter*_press_any_key_bliking_speed)%255)
        
        SURFACE.blit(_press_any_key, (WIDTH/2 - _press_any_key.get_width()/2, HEIGHT/5*4))
        
        
    SURFACE.blit(_title_text, _title_pos)



    #STATE 2
    if(general_control_state == 2):
        DrawCircles(circle_arr, _circle_position_x, _circle_position_y)
        is_input_start = True
        
        _input_number_text = system_font_small.render(input_number_str, True, WHITE)
        SURFACE.blit(_input_number_text, (_circle_position_x- _input_number_text.get_width()/2, _circle_position_y-_input_number_text.get_height()/2))

        #1. 시작
        if(input_number_str == '1'): 
            _menu_start = system_font_medium.render(MAIN_START_GAME, True, ORANGE)
            if(int(input_number_str) != highlight_btn_num_for_sfx):
                SoundCall('change_select')
                highlight_btn_num_for_sfx = int(input_number_str)
        else:
            _menu_start = system_font_medium.render(MAIN_START_GAME, True, WHITE)
        SURFACE.blit(_menu_start, (WIDTH/3*1 - _menu_start.get_width()/2, HEIGHT/5*2 - _menu_start.get_height()/2)) #얼라리근데 위치가 아 참


        if(input_number_str == '2'):
            _menu_start = system_font_medium.render("2. Info", True, ORANGE)
            
            if(int(input_number_str) != highlight_btn_num_for_sfx):
                SoundCall('change_select')
                highlight_btn_num_for_sfx = int(input_number_str)
            
            _sub_menu_count = 0
            _splited_info_msg = MAIN_START_INFO_MSG.split('\n')
            for _ in _splited_info_msg:
                _sub_menu_start = system_font_small.render(str(_), True, WHITE)
                SURFACE.blit(_sub_menu_start, (WIDTH/4*3 - _sub_menu_start.get_width()/2, HEIGHT/5*3 - _sub_menu_start.get_height()/2 + (_sub_menu_count-int(len(_splited_info_msg)/2))*_sub_menu_start.get_height())) #
                _sub_menu_count += 1
        else:
            _menu_start = system_font_medium.render("2. Info", True, WHITE)
        SURFACE.blit(_menu_start, (WIDTH/4*1 - _menu_start.get_width()/2, HEIGHT/5*3 - _menu_start.get_height()/2))
        

        if(input_number_str == '3'):
            _menu_start = system_font_medium.render("3. Really?", True, ORANGE)
            if(int(input_number_str) != highlight_btn_num_for_sfx):
                SoundCall('change_select')
                highlight_btn_num_for_sfx = int(input_number_str)
        else:
            _menu_start = system_font_medium.render("3. Exit", True, WHITE)
        SURFACE.blit(_menu_start, (WIDTH/4*1 - _menu_start.get_width()/2, HEIGHT/5*4 - _menu_start.get_height()/2))

        _sub_menu_start = system_font_small.render(f"{GAME_VERSION}", True, WHITE)
        SURFACE.blit(_sub_menu_start, (WIDTH - _sub_menu_start.get_width(), HEIGHT - _sub_menu_start.get_height()))
        



        if(is_input_end):
            is_input_end = False
            is_any_key_pressed = False
            if(input_number == 1): 
                PageChange(1)
            elif(input_number == 2): 
                print()
            elif(input_number == 3): 
                pg.quit()
                sys.exit()
        
    
            
#오늘은 진짜 여기까지

def DrawBattleLogBox(_pos_x, _pos_y, _size_x, _size_y):
    #높이:
    pg.draw.rect(SURFACE, BLACK, (_pos_x-_size_x/2, _pos_y-_size_y/2, _size_x, _size_y))
    pg.draw.rect(SURFACE, WHITE, (_pos_x-_size_x/2, _pos_y-_size_y/2, _size_x, _size_y), 5)

def BattleLogPush(_text):
    global battle_log_tick
    global battle_log

    _size_x = UI_BATTLE_LOG['size_x']
    _char_width, _char_height = battle_log_font.size('M')
    if(_text != '' ):
        _count = 0
        battle_log_tick = tick_counter
        _size_count = 0
        while(_text != ''):
            if(re.sub('[^가-힣]', '', _text[_count]) != ''):
                #한글

                _size_count +=2
                _count += 1

            elif(_text[_count] == '§'):
                _size_count -= 1
                _count += 1

            else:
                _size_count +=1
                _count += 1

            if((_size_count+3)*_char_width >= _size_x or _count >= len(_text)):
                del battle_log[0]
                battle_log.append(_text[:_count])
                _text = _text[_count:]
                _count = 0
                _size_count = 0

    

def DrawBattleLog(_speed = 1):
    '''
    _start_time : 말을 시작한 tick
    _text : 말할 내용 str
    _speed : 말하는 속도
    ... return : 대사 끝나는 tick_counter값 반환
    '''
    
    global battle_log
    global battle_log_tick

    _speed *= DIALOG_SPEED
    
    _char_width, _char_height = battle_log_font.size('M')
    _pos_x = UI_BATTLE_LOG['pos_x']
    _pos_x_center = UI_BATTLE_LOG['pos_x_center']
    _pos_y = UI_BATTLE_LOG['pos_y']
    _size_x = UI_BATTLE_LOG['size_x']
    _size_y = UI_BATTLE_LOG['size_y']
    DrawBattleLogBox(_pos_x_center,_pos_y,_size_x,_size_y)

    
            

        
    _dialog = battle_log[:]
    
    

    #마지막 텍스트 길이 지정

    _char_time_length = TICK_PER_SEC / _speed
    _current_time = tick_counter - battle_log_tick#진행된 시간
    _now_text_point = int(_current_time//_char_time_length)


    _dialog[-1] = _dialog[-1][:_now_text_point]


    _last_text_width = 0
    _word_color = DIALOG_COLORS['0']
    #아 생각해보니까 시간에 따라 자르는걸 안했네
    _is_center = False
    _count = 0
    _text_width = 0
    '''
    기능: 
    []의
    맨 뒤부터 한줄씩 출력
    근데 한 줄이 가로 길이를 넘으면 두줄로 치환해줌
    그냥 다시 써야지;;
    '''
    for _word in _dialog:
        if(_word != ''):
            _last_text_width = 0
            _word = _word.split('§')
            for i in _word:
                if(i != ''):
                    if(i == 'c'):
                        _is_center = True
                    elif(i == 'l'):
                        _is_center = False
                    else:
                        _text_width = 0
                        _text_width += (len(i)-1) * _char_width
                        _text_width += (len(re.sub('[^가-힣]', '', i))) * _char_width
                        if(i[0] in DIALOG_COLORS):
                            _word_color = DIALOG_COLORS[i[0]]
                            i = i[1:]
                        _text_surface = battle_log_font.render(i, True, _word_color)
                        _pos_y_check = _pos_y - _size_y/2 + _text_surface.get_height()/2 +_count*(_char_height + 5)
                        if(_is_center):
                            _text_pos = (_pos_x_center-(_text_width/2)+_last_text_width-_char_width, _pos_y_check)
                        else:
                            _text_pos = (_pos_x + _char_width + _last_text_width - _size_x/2, _pos_y_check)
                            
                        #이것때문인 것 같긴 한데
                        _last_text_width += _text_width
                        SURFACE.blit(_text_surface, _text_pos)


        _count+=1

                    



#def GenerateFormula(): 뭔가 통일성이 없네 그냥 main에 박아넣을까 굳이... global까지 써가면서 할 이유가... main이 좀 깨끗해지기는 하겠찌만... 음 음 ...
def DrawCircles(_arr, _x_pos = WIDTH/5, _y_pos = HEIGHT/5*4):
    for _x, _y, _r, _rs, _e, _s,in _arr: #스읍 이걸 어케할까
        DrawCircle(_x+_x_pos, _y+_y_pos, _r, _e, _s)

#NEED FIX : 원 막 변경(oppacity(alpha))도 되고 막 이렇구 저렇구 되게 그리고 원도 []말고 {}로 바꾸자 그냥
#circle... include x, y, rotate, rotateSpeed, effect, size, oppacity, oppacity_speed 
def DrawCircle(_x, _y, _rotate, _effects, _size):
    image_path = CIRCLES[_effects]
    image = pg.image.load(image_path)
    image = pg.transform.rotate(image, _rotate)
    image = pg.transform.scale(image, (image.get_size()[0]*_size, image.get_size()[1]*_size))
    image.get_rect().center = (image.get_size()[0], image.get_size()[1])
    image_rect = image.get_rect()
    image_size = image.get_size()
    
    SURFACE.blit(image, (_x-image_size[0]/2, _y-image_size[1]/2))

#NEED ADD : 마법진 투명도 및 색 변환 추가
def UpdateCircles():
    print()
    '''
    input : circles_arr
    output : return circles_arr(수정됨)
    '''

def DrawInputNumber(posX, posY):
    text_surface = formula_font.render(input_number_str, True, (255, 255, 255))
    SURFACE.blit(text_surface, (posX - text_surface.get_width()/2, posY - text_surface.get_height()/2))


def DrawFormula(_arr):
    #inital position draw formula
    _space = 2
    _formula = formula_font.render("1", True, WHITE)#아 근데 숫자가 2자릿수이면 그렇구나
    #counter
    _count = 0
    for i in _arr:
        if(type(i)==int):
            _count += len(str(i))
        else:
            _count += 1
    _draw_position_x = (WIDTH//5 - _count * (_formula.get_width()/2))

    _draw_position_y = HEIGHT//5
    _root_start_position_x = 0
    for i in _arr:
        if(type(i) == int):
            i = str(i)
        if(i == 'root'):
            #maybe... i need deepcopy........... this need CHANGE to DRAW LINE******** 

            _formula = formula_font.render("V", True, WHITE)
            SURFACE.blit(_formula, (_draw_position_x, _draw_position_y-2)) 
            _draw_position_x += _formula.get_width()#+_space
            _root_start_position_x = -5+_draw_position_x 
            #대충 root모양 씌우기 
            #대충 rootSwitch키고 슥슥하기
        elif(i == 'rootend'):
            pg.draw.line(SURFACE, WHITE, (_root_start_position_x, _draw_position_y-2), (_draw_position_x, _draw_position_y-2), 2)


        else:
            _formula = formula_font.render(i, True, WHITE)
            SURFACE.blit(_formula, (_draw_position_x, _draw_position_y)) 
            _draw_position_x += _formula.get_width()+_space
        #어? 근데 width가 fontsize랑 같으려나? -> 아님
        #moveDrawPoint 그러니까 여기서 글자 방금 쓴거 크기만큼 드로우 위치를 바꿔주는거지
        

def SoundCall(_sound, _volume = 1):
    '''소리 번호 입력하면 소리 출력해줌'''  
    _sound = mixer.Sound(SFX_PATH+SFX[_sound])
    _sound.set_volume(SFX_VOLUME * _volume)
    _sound.play()

def BgmCall(_bgm, _volume = 1):
    global now_bgm
    if(_bgm != now_bgm):
        now_bgm = _bgm
        _music = BGM[_bgm]
        mixer.music.set_volume(_volume * BGM_VOLUME)
        mixer.music.load(_music)
        mixer.music.play(-1) 
    if(_volume*BGM_VOLUME < mixer.music.get_volume()):
        mixer.music.set_volume(_volume+5)
    elif(_volume*BGM_VOLUME > mixer.music.get_volume()):
        mixer.music.set_volume(_volume*BGM_VOLUME)


def EventGenerator():
    #이 제네레이터가 따로 필요한 이유는 그 현재로써는 불가능한 얘들도 있잖아 조건이 안맞아서 그런 얘들을 걸러서 리스트로 정리하고 거기서 뽑아야 되니까!!
    #랜덤 이벤트가 없으니까 없애도 괜찮을 듯..?
    print()


#SpellMakers... prefix is S
'''
싹다 뒤집어
spell order...
1. level select
2. type, magnificant...etc
3. target Select

Init : 스펠 초기화

Recommand : 다음에 올 수 있는 스펠 고지
-> 마법 각 칸마다 띄워주는데 한 줄에 최대 3개

Append : 스펠 뒤에 더해가기
음 그냥 스펠 이름으로 해? 그게 알아먹기는 쉬울 듯

Maker : 마법을 합침...> 하나의 스펠로 압축

Trigger : 합친 마법 발동

S_... : 각 큐 마법에 해당하는 문제 제출기... return problem, answer
..-> 마법(문제) 실패시: 위력 감소, 자기 피해(마나 역류같은 뭐그런거), 마법 사라짐, -곱하기
'''
def SpellInit():
    '''
    return spell initial form
    '''
    spell_result = {
        "damage" : 0,
        "level" : 0,
        "type" : "normal",
        "effects" : {},
        "target" : "self",
    }
    return spell_result




#State Draw Function...
def KeyInput():
    global is_input_end
    global is_input_start
    global tick_input_end
    global next_page_state
    global is_enemy_hit
    global is_any_key_pressed
    global any_key_pressed_tick
    global is_input_wheel
    global input_wheel
    global info_scroll_count
    global input_number_str


    for _event in pg.event.get():
        #키 입력 처리
        if _event.type == pg.KEYDOWN:
            C_PressKey(_event.key, True)
        
            if _event.type == QUIT:
                print("현재 실수로 눌러서 끌 것 같아서 종료 기능을 꺼뒀습니다.")
                pg.quit() 
                sys.exit()
            if _event.type == pg.KEYDOWN:
                any_key_pressed_tick = tick_counter
                is_any_key_pressed = True
                
                if(is_input_start):
                    NumberInput(_event)
            
                

            if _event.key == pg.K_ESCAPE:
                print("현재 실수로 눌러서 끌 것 같아서 종료 기능을 꺼뒀습니다.")
                pg.quit()
                sys.exit()

        #키 때기 처리
        if _event.type == pg.KEYUP:
            C_PressKey(_event.key, False)


        if _event.type == pg.MOUSEBUTTONDOWN:
            if(is_input_wheel or info_window_state > 1):
                if _event.button == 4:  # 휠을 위로 돌렸을 때
                    input_wheel += 1
                elif _event.button == 5:  # 휠을 아래로 돌렸을 때
                    input_wheel += -1
                is_input_wheel = False


    if((is_input_wheel or is_input_wheel) and C_Delay("UpDownKey", tick_counter, 0.5)):
        #휠 및 위아래 입력
        if(C_PressedKeyCheck(pg.K_UP)):
            if(is_reverse_wheel):
                input_wheel -= 1
            else:
                input_wheel += 1
                if(info_window_state > 0 and input_number_str != '1'):
                    if(input_number_str == ''):
                        input_number_str = '1'
                    SoundCall('change_select_2',0.5)
                    input_number_str = str(int(input_number_str)-1)
        
        
        if(C_PressedKeyCheck(pg.K_DOWN)):
            if(is_reverse_wheel):
                input_wheel += 1
            else:
                input_wheel -= 1
                if(info_window_state > 0 and input_number_str != '9'):
                    if(input_number_str == ''):
                        input_number_str = '1'
                    SoundCall('change_select_2',0.5)
                    input_number_str = str(int(input_number_str)+1)
        is_input_wheel = False



        



def NumberInput(_event):
    global is_input_start
    global is_input_end
    global tick_input_end
    global input_number_str
    global input_number
    global is_input_num_minus
    global is_input_backspace
    # 숫자 키 입력 처리
    if(_event.key == pg.K_MINUS or _event.key == pg.K_KP_MINUS):
        is_input_num_minus = not is_input_num_minus

    if _event.key in NUMBER_KEYS.keys():
        if len(input_number_str)<input_number_length + is_input_num_minus:
            input_number_str += _event.unicode
        else:
            input_number_str = input_number_str[:-1]+_event.unicode
    
    #음수 표현
    if(len(input_number_str) > 0):
        if(is_input_num_minus and input_number_str[0] != '-'):
            input_number_str = '-' + input_number_str
        elif(not is_input_num_minus and input_number_str[0] == '-'):
            input_number_str = input_number_str[1:]
   #뭔가 배경이 어두우니까 좀 그런ㅁ데
    # 백스페이스 키 입력 처리
    if _event.key == pg.K_BACKSPACE:
        if(len(input_number_str) == 0):
            is_input_backspace = True
        input_number_str = input_number_str[:-1]
        

    # 엔터 키 입력 처리
    elif _event.key in RETURN_KEYS:
        if(input_number_str != ''):
            
            tick_input_end = tick_counter
            input_number = int(input_number_str)

            is_input_start = False#장실점
            is_input_end = True
            is_input_num_minus = False
        input_number_str = ''

def ShowFPS():
    _fps = round(FPSCLOCK.get_fps(),2)
    _fps_surface = dialog_font.render(str(_fps), True, WHITE)

    SURFACE.blit(_fps_surface,(WIDTH-_fps_surface.get_width(),HEIGHT-_fps_surface.get_height()))

def PageChange(_next_page):
    global next_page_state
    next_page_state = _next_page

def DisplayChange():
    global battle_log
    #battleLog setting
    _size_y = UI_BATTLE_LOG['size_y']
    _char_width, _char_height = battle_log_font.size('M')
    battle_log = ['']
    for i in range(int(_size_y//(_char_height+5))-1):
        battle_log.append('')

def main():
    #init setting
    global is_input_start
    global is_input_end
    global input_number_str
    #page Setting
    global now_page_state #page_state... 0,1,2... [MainPage(booting Game), AdvanturePage, CombatPage, ...]
    global next_page_state  
    #ForChangeDisplay... 'is' is arrow "bool"
    global is_changing_page_state    
    global is_page_change_on
    global page_change_count
    global is_draw_formula
    global general_control_state


    global event_tick
    

        

    #startBGM
    DisplayChange()
    
    
    
    

    #아니... 굳이 코루틴이 필요할까? 아니...없을지도 몰라 그냥 소리 줄이고 늘리고 하는것도 화면 이동이랑 같이 쓰면 되는 것 아니겠어... 그치 화면 이동중에 바뀌겠지 음음 그래 코루틴 따윈
    #필요가 없는거야 모르면 ㅁ ㅝ다? 안쓰면 된다~ 아니 배우긴 해야하는데 아니 지금까지 많이 써어ㅗㅆ는데도 머리가 어질하네
    while True:
        global tick_counter
        tick_counter += 1
        SURFACE.fill((0, 0, 0))
        
        KeyInput()

        #Page Controller
        if(now_page_state == 0):
            P_MainmenuDraw()

        elif(now_page_state == 1):
            P_AdventureDraw()

        elif(now_page_state == 2):
            P_BattleDraw()
            



        #updateCircle...
        for i in range(len(circle_arr)):
            circle_arr[i][2] += circle_arr[i][3]


        #pageChange... 
        if(now_page_state != next_page_state or is_changing_page_state):
            is_changing_page_state = True
            _surface = pg.Surface((WIDTH, HEIGHT))
            _surface.fill((0,0,0))

            
            if(not is_page_change_on):
                is_page_change_on = True
                page_change_count = tick_counter


            if(tick_counter < page_change_count + int(TICK_PER_SEC * FADE_LENGTH) and now_page_state != next_page_state):
                #is_page_change_on = False
                mixer.music.set_volume(BGM_VOLUME - BGM_VOLUME*(tick_counter - page_change_count)/(TICK_PER_SEC * FADE_LENGTH))
                _surface.set_alpha(((tick_counter - page_change_count)/(TICK_PER_SEC * FADE_LENGTH)) * 255)
                SURFACE.blit(_surface, (0,0))

            elif(tick_counter == page_change_count + int(TICK_PER_SEC * FADE_LENGTH) and now_page_state != next_page_state):
                mixer.music.set_volume(0)
                _surface.set_alpha(255)
                SURFACE.blit(_surface, (0,0))
                event_tick = tick_counter + TICK_PER_SEC * FADE_LENGTH * 1 
                now_page_state = next_page_state
                page_change_count = tick_counter
                general_control_state = 0
                is_input_end = False

            elif(tick_counter < page_change_count + int( TICK_PER_SEC * FADE_LENGTH)):
                
                #mixer.music.set_volume(BGM_VOLUME*(tick_counter - page_change_count)/( TICK_PER_SEC * FADE_LENGTH))
                _surface.set_alpha(255-((tick_counter - page_change_count)/(TICK_PER_SEC * FADE_LENGTH) * 255))
                SURFACE.blit(_surface, (0,0))
                
                
            else:
                #mixer.music.set_volume(BGM_VOLUME)
                
                is_changing_page_state = False
                is_page_change_on = False

            
            
            
            #surface
            
            
        ShowFPS()
        
        O_SURFACE.blit(pg.transform.scale(SURFACE, O_SURFACE.get_rect().size), (0,0))
        pg.display.flip()#-> 다 지우고서 그림
        
        all_sprites.draw(SURFACE)
        FPSCLOCK.tick(TICK_PER_SEC)
        
        

if __name__ == '__main__':
    main()



