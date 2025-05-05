import pygame as pg

# game options/settings 
TITLE = "TEST"
'''
WIDTH = 1280
HEIGHT = 720

WIDTH = 1920
HEIGHT = 1080


현재 1920, 1080에 최-적화 되어있슴니다
화면이 깨져도 정상적인 플레이를 원한다면 
O_WIDTH, O_HEIGHT에 모니터 가로 세로를 각각 입력하시고
난 화면이 깨지는 걸 원치 않는다 하면 WIDTH, HEIGHT도 함께 바꿔주십시오

... 모르겠다 싶으면 

이 아래 코드를  '#이곳에 입력'을 지우고 삽입
O_WIDTH, O_HEIGHT = 1280, 720


'''
O_WIDTH = 1920
O_HEIGHT = 1080

#이곳에 입력... (또는 밑 코드 #만 지우기)
#O_WIDTH, O_HEIGHT = 1280, 720
WIDTH = 1920
HEIGHT = 1080


FPS = 30

INF = 10**9

#Preset Player properties
PRE_PLAYER_HEALTH = 100
PRE_PLAYER_SHIELD = 0

PRE_PLAYER_INT = 5
PRE_PLAYER_DEX = 5
PRE_PLAYER_STR = 5
PRE_PLAYER_WIS = 5

PRE_PLAYER_SPELLTIME = 100
PRE_PLAYER_EFFECTS = []
PRE_PLAYER_MAXSPELL = 3
PRE_PLAYER_FORMULA_LEVEL = 1
PRE_PLAYER_MONEY = 0
PRE_PLAYER_FOCUS = 100
PRE_PLAYER_STAMINA = 100

#circle_size_weight
CIRCLE_SIZE = 1

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LITTLE_RED = (240,86,80)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 127, 39)
SKY = (0, 255, 255)
BROWN = (150, 75, 0)
DEEP_GRAY = (40, 40, 40)
DEEP_BLUE = (0, 0, 128)
GRAY = (128, 128, 128) #와 머야 개쩐다
DIALOG_COLORS = {'0' : WHITE, 
                 '1' : RED, 
                 '2' : ORANGE,
                 '3' : YELLOW,
                 '4' : GREEN,
                 '5' : BLUE,
                 '6' : SKY,
                 '7' : BROWN,
                 '8' : LITTLE_RED,
                 '9' : DEEP_GRAY,
                 'q' : DEEP_BLUE,
                 'w' : GRAY,
                 }

#먼가 이런것도 규칙이 있어야 간지남
#BIG.Medium.small
#t: test...
#v: all right.
GAME_VERSION = "0.0.0t"

#misic
KOR_FONT = "data\\fonts\\GalmuriMono11.ttf"
TICK_PER_SEC = FPS
FADE_LENGTH = 0.5
DIALOG_SPEED = 200
DIALOG_POS_Y = 5


MAIN_PAGE_NUM = 0
ADVENTURE_PAGE_NUM = 1
BATTLE_PAGE_NUM = 2




#KEY
RETURN_KEYS = [pg.K_KP_ENTER, pg.K_RETURN]

NUMBER_KEYS_CONFIGURE ={
    0: [pg.K_KP0, pg.K_0],
    1: [pg.K_KP1, pg.K_1],
    2: [pg.K_KP2, pg.K_2],
    3: [pg.K_KP3, pg.K_3],
    4: [pg.K_KP4, pg.K_4],
    5: [pg.K_KP5, pg.K_5],
    6: [pg.K_KP6, pg.K_6],
    7: [pg.K_KP7, pg.K_7],
    8: [pg.K_KP8, pg.K_8],
    9: [pg.K_KP9, pg.K_9]
}
NUMBER_KEYS = {}
for num, key in NUMBER_KEYS_CONFIGURE.items():
    for i in key:
        NUMBER_KEYS[i] = num

KEY_PLUS = [pg.K_KP_PLUS, pg.K_KP_PLUS]
KEY_MINUS = [pg.K_KP_MINUS, pg.K_KP_MINUS]
KEY_DIVIDE = [pg.K_KP_DIVIDE, pg.K_KP_DIVIDE]
KEY_MULTIPLY = [pg.K_KP_MULTIPLY, pg.K_KP_MULTIPLY]

#SOUND

#Volume
BGM_VOLUME = 0.6
SFX_VOLUME = 0.6


#UI SIZE AND POS 
UI_ADVENTURE_TOP_BAR = {'pos_x': WIDTH/5*2,'pos_y': 0, 'size_x': WIDTH/5*3,'size_y' : HEIGHT/16}
BATTLE_BUTTON = {'size_x' : WIDTH/18*2, 'size_y' : HEIGHT/18*1}
COOLTIME_BAR = {'pos_x': WIDTH/5*3.5,'pos_y': 0, 'size_x': WIDTH/5*2.5, 'size_y' : HEIGHT/16}
UI_SKILL_BATTLE = {'pos_x': WIDTH/20*1,'pos_y': 0, 'size_x': WIDTH/5*2 - WIDTH/20*1, 'size_y' : HEIGHT/2}
UI_BATTLE_LOG = {'pos_x' :WIDTH/5*3.5, 'pos_x_center' : WIDTH/5*3.5, 'pos_y' : HEIGHT/12*10, 'size_x' : WIDTH/5*3-WIDTH/10, 'size_y' : HEIGHT/4}
UI_INFO_WINDOW = {'pos_x' : WIDTH/5*3, 'pos_y' : HEIGHT/2,'size_x': WIDTH/8*5, 'size_y' : HEIGHT/4*3}#저녁먹어야지

BACKGROUND_COLOR = BLACK
HIGHLIGHT_COLOR = ORANGE
BUTTON_COLOR = WHITE

#BackGroundMusicPack.. this is equal to mapNumber!
#1. ExampleSound.. 
#http://amachamusic.chagasi.com/
INFO_MENUS = ['1.가방', '2.기술', '3.상태', '4.닫기']

BGM = {
        0: "Example.mp3",
        "AdventureMenu": "die2.mp3",
        "test" : "tinkle horror.wav",
        "boss" : "Battle3.mp3",
        "MainMenu" : "orgol.mp3", 
        "eForest" : "rainforest.wav",
        "eFrog" : "Frogs-Lisa_Redfern-1150052170.wav",
        "eBird" : "mixkit-morning-birds-2472.wav",
        "normal_enemy" : "Battle.mp3",
        "eCaveWater" : 'dripping-water-in-cave-114694.mp3',
        "orgol" : "die3.mp3"
        #잠깐 장실점
    }


for a,b in BGM.items():
    BGM[a] = "data\\bgm\\"+b
    
#sfx
SFX_PATH = "data\\sfx\\"
SFX = {0:"Success.wav",
       1:"Fail.wav",
       'change_select': "change_select.wav",
       'press_start' : "clean bell_orange.mp3",
       'change_select_2' : "change_select_small.wav",
       'bash_1' : 'clean-fast-swooshaiff-14784.mp3',
       'bash_2' : 'sword-sound-2-36274.mp3',
       'sword_crash' : 'sword-hit-7160.mp3',
       'sword_smash' : 'draw-sword1-44724.mp3',
       
       }


#IMAGE
#Image Path for System
IMAGE_PATH = 'data\\img\\'
HEALTH_BAR_PATH = IMAGE_PATH+'HealthBar.png'
HEALTH_BAR_CASE_PATH = IMAGE_PATH + 'HealthBarCase.png'

BTN_BATTLE_MAGIC_PATH = IMAGE_PATH + 'Choice_Magic.png'
BTN_BATTLE_MAGIC_HIGHLIGHT_PATH = IMAGE_PATH + 'Choice_Magic_HighLight.png'

BTN_BATTLE_CHECK_PATH = IMAGE_PATH + 'Choice_Check.png'
BTN_BATTLE_CHECK_HIGHLIGHT_PATH = IMAGE_PATH + 'Choice_Check_HighLight.png'

MAIN_TITLE_IMAGE_PATH = IMAGE_PATH + 'title_.png'

CIRCLES = {'normal_white' : "circle.png",
           'normal_red' : "circle_red.png",
           'normal_red_square' : "circle_red_sq.png",
           'normal_white_square' : "circle_sq.png"
           }
for a, b in CIRCLES.items():
    CIRCLES[a] = IMAGE_PATH+b
