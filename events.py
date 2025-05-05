
#prefix 'E' is Event
#연속 이벤트의 경우(대화창이 2번 이상 나타나는 이벤트)
#E_Test_1 -> E_Text_1_1(선택지 1번)
#E_Test_1 -> E_Text_1_2_1(선택지 2번 선택 후 이후 이벤트에서 1번 선택(3장면) 아 밥먹었으니 장실저 ㅎ.ㅎ...)

#아니면 그냥 class하나로 이벤트를 끝낼까? def안에서 또 선택지를 주고 해서 하면 될 것 같기도 한데
#NEED ADD Select Text도 색 바꾸기
'''
NEED FIX 또는 NEED ADD : 나중에 고칠 부분 빠르게 찾기 위해 다는 주석
**매우 중요 : 매 이벤트마다 self.effects 초기화 무ㅜㅜㅜㅜㅜㅜㅜㅜㅜ조건!!!!!!!!!!!!!!!!!!!!!

dialog prefix
!!only first
§l : 좌측 정렬
§r : 안만듦
§c : 가운데 정렬

!!anywhere, i >= 1
§1 : red
§2 : blue
§3 : green
§4 : black
§0 : white 


전투가 끝난 후 어떻게 할까?
1. 원래 화면으로 돌아오기
2. 기존 있던 지역 다시 출입하기
3. 스읍...2가 맞겠지가 아니 아 그래 이동중 전투는 이동 후 위치로 이동하고
일부로 찾아서하는 전투는 끝나고 그 장소로 다시 이동하는거야


effects 내부 name목록
getItem - value(id) - count
damage - value
battle - {monster}

needs 내부 name 목록
haveTool






bgm : 맵 테마 음악
percent : 맵 랜덤 출현 확률 (1~100)...근데 하다보면 그다지 안 쓸 것 같기도 함
needState : 해당 맵 
time : 이동시간
prefixDialog : Dialog 앞부분
dialog : 메인
suffixDialog : Dialog 뒷부분에 덧붙이기. 플레이어 소지 및 스테이터스를 체크하기 위해 따로 제작
isEnd = __init__에서는 False. isEnd()에서는 True
Area : 좁은 범위 위치(상점가 3번지)
Region : 넓은 범위 위치(히포크라테스 마을)


eventCheck : __init__에서는 False, 이외 모든 Sel1()...에서는 모두 True -> effects 적용해주는거임
cell : 위치 카운터 개념(던전을 깊숙히 들어가는 그런 것)

그외는 모두 임시 함수. 그리고 임시 함수는 "절대" main을 통해 연산하지 말 것. -> 오류.. 9.8추가) geattr인가 로 하면 예외 오류 해결 가능할 듯? NEED FIX
event 내에서 알아서 처리할 것

월드벨류
name key data


'''
from custom_operator import *
from settings import *
from items import *
from sprites import *



#NEED FIX : player가 sprites안에 있음. 전체적으로 get, set 없애고 직접 확인으로 교체...-> 상당히...상당히 오래 걸릴 듯? 

class E_Death():
    def __init__(self):
        self.eventName = '이야기의_종착지'
        self.bgm = "AdventureMenu"
        self.percent = 0
        self.needState = [{}]
        self.time = 5
        self.suffixDialog = []
        self.prefixDialog = []
        self.selections = [{"function": self.End,
                            "text": "다시 이야기에 집중한다.",
                            "needs": []},] 
        self.isEnd = False
        self.isBattle = False
        self.isEventCheck = False
        self.nowCell = ''
        self.cells = []
        self.effects = []

        self.area = '???'
        self.region = '???'

        '''
        '§l§0"... 당신의 이야기는 이렇게 끝났습니다. 아, 물론 당신도 알잖아요? 진짜 이야기는 안 끝났다는 거. 좀 더 들어봐요. 이제 시작이라구요."\n'
        '§l§0"자, 그럼 다시... 흠흠!"\n\n\n'
        '§c§6"...사실, 당신은 알고 있었습니다. 이 이야기가 여기서 끝날 리 없단걸요. \n'
        '§c§6눈 먼 시계침은 제 역할을 거스르고, 이야기는 다시금 시작됩니다."\n\n\n'
        '''

        #나중에 여기서 막... 아에 모든 걸 거슬러 올라가는거야 스읍 좀 맘에 안드는데
    def DialogSet(self, event):
        event.__init__()
        self.dialog = (
                        '§c§0...이야기가 멈췄다.\n'
                        '§c§0나는 알고있다. 아직 이야기는 끝나지 않았다는 걸.\n\n\n'
                        '§c§0.\n'
                        '§c§0.\n'
                        f'§c§0"{event.dialog[2:15]}..."\n'
                       )
        self.effects = []
    def End(self):
        self.isEnd = True
    

class E_Tutorial():
    def __init__(self):
        self.bgm = "AdventureMenu"
        self.percent = 0
        self.needState = [{}]
        self.time = 5
        self.eventName = '튜토리얼'
        self.prefixDialog = [{"text": '',
                                "needs" : [],
                                }]
        #dialog를 시간단위로 다르게 작성할까... 그건 나중에
        self.dialog = ('§l§0 당신과 여동생은 한 번 떠났다 하면 몇달을 돌아오지 않는 모험가 부부를 부모로 두고 있습니다. '
                       '이미 어릴 적부터 부모를 기다리는 데에는 이골이 났기 때문에, 여느때처럼 집에서 기다리던 날이었습니다. '
                       '이날, 아침 일찍부터 당신은 자는 동생을 뒤로하고 수련 겸 나무를 하러 근처 숲 속으로 들어왔습니다.\n'
                       '.\n'
                       '.\n'
                       '.\n'
                       '§l§0당신의 부모님 말로는 숲에 마물이 있기에 나무를 한다면 꼭 이 근처에서 하라고 했습니다. '
                       '당신은 언제나 호기심이 들지만, 마물과 마주치면 곤란할 것을 알고 있습니다. '
                       '그렇기에 당신은 숲에 깊게 들어가지 않고 나무를 물색합니다.\n'
                       '이 나무가 적당해 보입니다.\n'
                       )
        

        self.suffixDialog = [{"text": '',
                                "needs" : [],
                                }]
        self.isEnd = False

        self.region = '하이델 숲'
        self.area = '벌목지'
        self.nowCell = ''

        self.selections = [{"function": self.Sel0_BattleStart,
                            "text": "으랴! (전투)",
                            "needs": []}, 
                           ]
        
        self.effects = [{"name":"damage", "value":"0"}]
        self.isBattle = False
        self.isEventCheck = False
    
    def Sel0_BattleStart(self):
        self.dialog = ('§l§1\n')
        
        self.effects = [{"name" : "damage", "value" : "0"}, 
                        {"name" : "battle", "enemies": [{'enemy' : M_TutorialTree, 'chance' : 100}, {'enemy' : M_PariahDog, 'chance' : 0}]}]
        
        self.callEndFuntion = self.Sel0_BattleEnd
        self.isEventCheck = True
        self.isBattle = True

    def Sel0_BattleEnd(self):
        self.dialog = ('§c§0*쩌저적!*\n'
                        '§l§0큰 소리와 함께 나무가 넘어갑니다.\n')
        self.effects = []
        self.isBattle = False
        self.isEventCheck = True
        self.selections = [{"function": self.Sel1,
                            "text": "나무를 줍는다.",
                            "needs": []}, 
                           ]
        
    def Sel1(self):
        self.area = '집'
        self.dialog = ('§c§0.\n'
                       '§c§0.\n'
                       '§l§0당신은 나무를 잔뜩 지고 집으로 걸어갑니다. 벌써 하늘이 어둡습니다.\n'
                       '§l§0그런데 돌아온 집에는 여동생도, 따뜻한 카레도 없었습니다. 나와서 둘러봤지만 어디에도 여동생은 보이지 않았습니다. '
                       '§0주변이라면 숲 뿐인 곳이라 아마 숲 어딘가에서 길을 잃은 것일지도 모릅니다. 벌목터라면 당신이 이미 지나온 길이기에 여동생은 깊은 숲 속 어딘가에 있으리라 결론지었습니다. '
                       '§0왜 숲에 들어갔을지는 모르겠지만, 당신은 여동생을 찾으러 가고자 준비합니다. 주방에서 몇개의 물약을 찾아냈지만, 무기가 없습니다. 도끼는 날이 무디고 무겁기에 미덥지 않습니다.\n\n'
                       '§l§0당신은 무기를 찾으려고 집 안을 살펴보다...\n'
                       )
        self.effects = [{"name":"damage", "value":"0"}]
        self.selections = [{"function": self.Sel1_1,
                            "text": "목검을 발견한다.",
                            "needs": []}, 
                            {"function": self.Sel1_2,
                            "text": "나무 지팡이를 발견한다.",
                            "needs": []}, 
                        ]
        self.isEventCheck = True
        
    def Sel1_1(self):
        self.dialog = ('§l§0안방의 옷장에서 목검을 발견했습니다. 엉성하지만, 두 손을 이용해 검을 잡아봅니다. 가끔 아버지가 검에 대해 알려주었던 것이 생각납니다.'
                       '분명 부모님을 기다린다면 나가기는 쉬울테지만, 그 양반들이 언제 돌아올 지 모르는데다 여동생에 대한 생각이 당신을 가만 있도록 두지 않습니다. '
                       '사실, 여동생이 도망 하나는 재빨랐기에 제 아무리 들개든, 늑대래도 괜찮으리라 생각했습니다. 다만... 길치였습니다.\n\n'
                       '§l§0천으로 목검을 둘러 등에 매고 뒤돌아 나갑니다.\n\n'
                       
                       )
        self.effects = [{"name" : "modifyState", "value" : "str", 'amount': 1}]
        self.selections = [{"function": self.EnterForest,
                            "text": "집을 떠난다",
                            "needs": []}, 
                            
                        ]
        self.isEventCheck = True

    def Sel1_2(self):
        self.dialog = ('§l§0안방의 탁자에서 작은 지팡이를 발견했습니다. 여차하면 몽둥이로도 쓸만해 보입니다. 가끔 어머니가 마법에 대해 알려주었던 것이 생각납니다. '
                       '분명 부모님을 기다린다면 나가기는 쉬울테지만, 그 양반들이 언제 돌아올 지 모르는데다 여동생에 대한 생각이 당신을 가만 있도록 두지 않습니다. '
                       '사실, 여동생이 도망 하나는 재빨랐기에 제 아무리 들개든, 늑대래도 괜찮으리라 생각했습니다. 다만... 길치였습니다.\n\n'
                       '§l§0지팡이를 벨트에 찔러넣고 뒤돌아 나갑니다.\n\n'
                       )
        self.selections = [{"function": self.EnterForest,
                            "text": "집을 떠난다",
                            "needs": []}, 
                        ]
        self.effects = [{"name" : "modifyState", "value" : "int", 'amount': 1}]
        self.isEventCheck = True

    def EnterForest(self):
        self.effects = [{"name":"damage", "value":"0"}, {"name" : "appendEvent", "value" : E_ForestNearHeidel}]
        self.isEventCheck = True
        self.End()

    def End(self):
        self.isEnd = True


class E_ForestNearHeidel():
    def __init__(self):
        self.percent = 5
        self.needState = {}
        self.cell = 0
        self.eventName = '하이델_숲'
        
        
        #NEED FIX : 이거... 좀 아름답게 고치거나 아에 플레이어한테 cell value 편입시키기
        self.area = '산길'
        self.region = '하이델 숲'
        self.effects = [{"name":"damage", "value":"0"}]
        self.isBattle = False
        self.isEventCheck = False
        self.bgm = "eForest"
        self.needState = {}
        self.prefixDialog = [{"text": '주위에 자를 나무가 많아 보입니다...\n',
                                "needs" : [{'name' : "haveTool", 
                                            'value': 'Cutting'}],
                                'else' : '주위에 벨만 한 나무가 많아보이지만, 도끼를 두고 왔습니다.\n'
                                }]
        self.dialog = ('§l§0당신은 길쭉한 나무로 가득찬 숲 속을 걷고 있습니다. 한낮이건만 나무에 그늘져 꼭 밤길같습니다.'
                       '주변에선 새가 지저귀는 소리가 들려옵니다. 어렴풋이 울부짖는 소리도 들려옵니다. 당신은 무기를 꽉 움켜쥡니다.'
                       '당신은 평화로워 보이는 이곳에 어떤 녀석들이 살고 있는지 잘 알고 있습니다. 정신나간 개라던가...\n'
                       '§c§0\n'
                       '§c§0\n'
                       '§c§0\n')
        
        self.suffixDialog = []
        self.isEnd = False 
        #NEED FIX : 이거... 좀 아름답게 고치거나 아에 플레이어한테 cell value 편입시키기

    
        self.cells = ['숲의 입구','숲 - 1','숲 - 2','숲 - 3','숲 - 4','숲의 출구']
        self.nowCell = self.cells[0]

        self.isBattle = False
        self.callEndFuntion = self.End
        self.reset()

    #reset이라기보단 redraw에 가까움
    def reset(self):
        self.bgm = "eForest"
        self.needState = {}
        self.dialog = ('§l§0당신은 길쭉한 나무로 가득찬 숲 속을 걷고 있습니다. 한낮이건만 나무에 그늘져 꼭 밤길같습니다.'
                       '주변에선 새가 지저귀는 소리가 들려옵니다. 어렴풋이 울부짖는 소리도 들려옵니다. 당신은 무기를 꽉 움켜쥡니다.'
                       '당신은 평화로워 보이는 이곳에 어떤 녀석들이 살고 있는지 잘 알고 있습니다. 정신나간 개라던가...\n'
                       '§c§0\n'
                       '§c§0동생의 발자국으로 추정되는 것이 한줄로 쭉 이어져 있습니다. 길을 잃었다기엔 어딘가 목적이 있는 것처럼 보입니다.\n'
                       '§c§0\n')
        

        self.isEnd = False 
        ''' 테스트용 코드
        self.selections = [{"function": self.Sel1,
                            "text": "나무를 벤다.",
                            "needs": [{'name' : "haveTool", 
                                       'value': 'Cutting'},
                                       {'name': 'hide', 'value' : False}]}, 

                            
                           ]
        '''
        self.selections = []
        
        if(self.nowCell != self.cells[-1]):
            self.selections.append({"function": self.CellUp,
                            "text": "발자국을 따라 나아간다.",
                            "needs": [{'name' : 'cellDown', 
                                       'value' : 9},
                                       {'name': 'hide', 
                                        'value' : True},
                                        ]})
        else:
            self.selections.append({"function": self.ExitToOut,
                            "text": "숲의 밖까지 이어진 발자국을 따라간다.",
                            "needs": [
                                       {'name': 'hide', 
                                        'value' : True},
                                        ]})


        if(self.nowCell != self.cells[0]):
            self.selections.append({"function": self.CellDown,
                            "text": "뒤로 돌아간다.",
                            "needs": [{'name' : 'cellUp', 
                                       'value' : 1},
                                       {'name': 'hide', 
                                        'value' : True}]})
        else:
            self.selections.append({"function": self.ExitToIn,
                            "text": "집으로 돌아간다.",
                            "needs": [
                                       {'name': 'hide', 
                                        'value' : True}]})

        if(C_TorF(35)):
            self.dialog += ('소리를 질러봐도 메아리칠 뿐 동생이 답하는 일은 없습니다. 다만 동물이 울부짖는 소리로 화답합니다.\n')
        #NEED FIX : 이거... 좀 아름답게 고치거나 아에 플레이어한테 cell value 편입시키기
        #아 그냥 events에서만 쓰는 변수들 좀 만들까 아 그럼 근데 또 코드가 더럽고 좀 그래
        



        self.isBattle = False
        self.isEventCheck = False


    def CellUp(self):
        self.Move(1)

    def CellDown(self):
        self.Move(-1)

    def Sel1(self):
        self.dialog = ('§l§0쓰 러진다~\n'
                       '§l§1Dead End\n'
                       )
        self.effects = [{"name":"", "value":"0"}]
        self.selections = [{"function": self.End,
                            "text": "으악",
                            "needs": []}, 
                        ]
        self.isEventCheck = True

    def Move(self, _vector):
        _cell_value = self.cells.index(self.nowCell)
        self.nowCell = self.cells[_cell_value + _vector]
        if(C_TorF(25)):
            self.IncounterMonster()
        else:
            self.reset()
        
        
    def ExitToOut(self):
        self.prefixDialog = [{"text": '', "needs" : [],}]
        self.suffixDialog = [{"text": '', "needs" : [],}]
        self.dialog = ('§l§0 숲의 출구가 보입니다. 발자국은 숲의 바깥까지 이어져 있습니다. 여동생은 도대체 어디로 가버린 걸까요.\n')
        self.effects = [{"name" : "appendEvent", "value" : E_PaibaRoad}]
        self.isEventCheck = True
        self.selections = [{"function": self.End,
                            "text": "숲에서 나가 발자국을 쫓는다.",
                            "needs": []}, ]
        
    def ExitToIn(self):
        self.dialog = ('§l§0 집이 보입니다. 하지만 아직 여동생을 찾지 못했습니다. 당신은 다시 발을 돌립니다.\n')
        self.selections = [{"function": self.reset,
                            "text": "다시 숲으로 들어간다.",
                            "needs": []}, ]

        self.effects = []
        self.isEventCheck = True

    def IncounterMonster(self):
        self.prefixDialog = [{"text": '', "needs" : [],}]
        self.suffixDialog = [{"text": '', "needs" : [],}]
        self.dialog = ('§c§1근처의 수풀 속에서 불길한 소리가 들려옵니다...\n'
                       '§l§1\n'
                       )
        self.effects = []
        self.selections = [{"function": self.Sel2_BattleStart,
                            "text": "싸움을 준비한다!",
                            "needs": []}, 
                        ]
        
    def Sel2_BattleStart(self):
        self.dialog = ('§l§1\n')
        
        self.effects = [{"name" : "damage", "value" : "0"}, 
                        {"name" : "battle", "enemies": [{'enemy' : M_PariahDog, 'chance' : 100}]}]
        
        self.callEndFuntion = self.Sel2_BattleEnd
        self.isBattle = True
        self.isEventCheck = True
        
    def Sel2_BattleEnd(self):
        self.effects = []
        self.isBattle = False
        self.isEventCheck = True
        self.callEndFuntion = self.Sel2_BattleEnd
        self.reset()
        
    def End(self):
        self.isEnd = True


class E_PaibaRoad():
    def __init__(self):
        self.eventName = '하이델_표지판사거리'
        self.percent = 5
        self.needState = {}
        self.cell = 0
        self.area = '갈림길'
        self.region = '하이델'
        self.effects = [{"name":"damage", "value":"0"}]
        self.isBattle = False
        self.isEventCheck = False
        self.bgm = "eBird"
        self.needState = {}
        self.dialog = ('\n')
        
        self.prefixDialog = []
        self.suffixDialog = []
        self.isEnd = False 

    
        self.cells = ['숲의 출구','이정표 앞']
        self.nowCell = self.cells[0]

        self.isBattle = False
        self.callEndFuntion = self.End
        self.reset()
        

    #reset이라기보단 redraw에 가까움 근데 이게 더 어감이 좋음 아니 사실 reset에 가깝나
    def reset(self):
        self.bgm = "eBird"
        self.needState = {}
        self.dialog = ('§l§0숲을 빠져나와 걷다보니 자갈길이 깔려있어 발자국이 보이지 않습니다. 저 멀리 이정표가 서있는 것이 보입니다. '
                       '당신이 숲 밖으로 나온 건 처음이었습니다. 동생이 어디로 갔을지도 짐작되는 바가 없어 우선 이정표부터 보러가기로 했습니다.\n'
                       
                       )
        
        
        self.addtionalDialog = []
        self.isEnd = False 
        self.selections = [{"function": self.Sel1_Milestone,
                            "text": "이정표를 살펴본다",
                            "needs": []}, 
                            
                            
                           ]

        self.isBattle = False
        self.isEventCheck = False
        self.callEndFuntion = self.End

    #이전 장소에서 올때 적용되는 변수들 적용
    def ComeInCheck(self, _event): 
        if(_event.eventName == '파이바_마을'):
            self.RoadToPaiba()#Load Cells
            self.nowCell = self.cells[-1]
            self.RoadToPaiba()#Apply Cell
        elif(_event.eventName == '디크_동굴'):
            self.RoadToCave()#Load Cells
            self.nowCell = self.cells[-1]
            self.RoadToCave()#Apply Cell

    def Sel1_Milestone(self):
        self.area = '갈림길'
        self.dialog = ('§l§0당신은 이정표까지 걸어갔습니다.'
                       '이정표에는 이렇게 쓰여 있습니다.\n'
                       '§c§7^\n'
                       '§c§7l\n'
                       '§c§7다리\n'
                       '§c§7<-- 디크 동굴    \n'
                       '§c§7    파이바 마을 -->\n'
                       '§c§7.\n'
                       '§c§7.\n'
                       '§c§0당신은 이정표를 지긋이 바라보며, 어디로 갈까 고민합니다.\n')
        
        self.prefixDialog = [{"text": ('§l§0 숲 속에서만 살아온 당신에겐 모두 생소한 지명 뿐입니다. 당신의 부모님은 모험가이건만 '
                                        '당신은 지금껏 모험은 고사하고 숲 밖으로 산책조차 나온 적 없습니다. 책으로 세상을 접한 것이 전부입니다. 어쩌면 바깥 세상엔 아무도 없는 것이 아닐까하며 '
                                        '살아온 당신입니다. 이런 생각은 뒤로하고, 당신은 동생은 어디로 향했을지 생각합니다.\n'),
                                "needs" : [{'name' : "getWorldValue", 
                                            'key': 'is_visited_milestone_1',
                                            'data' : False},],
                                'else' : ('§l§0 자세히 살펴보니 디크 동굴에 자그만 표식이 있습니다. 칼로 낸 흔적 같습니다.\n')
                                }]
        
        
        self.selections = [{"function": self.RoadToPaiba,
                            "text": "파이바로 이동한다.",
                            "needs": []},
                            {"function": self.RoadToCave,
                            "text": "동굴로 이동한다.",
                            "needs": []}, 
                            {"function": self.RoadToBridge,
                            "text": "다리로 이동한다.",
                            "needs": []},  
                           ]
                           
        self.effects = []
        self.isEventCheck = True

    def RoadToCave(self):
        self.region = '하이델'
        self.area = '동굴로 가는 길'
        self.cells = ['1', '2', '3', '동굴 앞']
        self.selfDef = self.RoadToCave
        self.defCode = 2
        self.prefixDialog = []
        self.selections = [
                           ]
        self.suffixDialog = []
        
        
        if(self.nowCell not in self.cells):
            self.nowCell = self.cells[0]

        if(self.nowCell != self.cells[-1]):
            self.selections.append({"function": self.CellUp,
                            "text": "동굴을 향해 이동한다.",
                            "needs": []})
            self.dialog = ('§l§0당신은 동굴로 걸어가고 있습니다. '
                           '멀리 보이는 동굴 주위를 강이 둘러싸고 있습니다. \n')
        else:
            self.selections.append({"function": self.EnterDikeuCave,
                                    "text": "동굴 안으로 들어간다.",
                                    "needs": []})
            self.dialog = ('§l§0 거대한 입구를 가진 동굴이 눈 앞에 보입니다. '
                           '주변으로 흐르는 강에선 세찬 물소리가 들려옵니다. 바람이 동굴 안으로 미약하게 불고 있습니다. \n')
            
            
        if(self.nowCell != self.cells[0]):
            self.selections.append({"function": self.CellDown,
                            "text": "이정표가 있는 갈림길 쪽으로 이동한다.",
                            "needs": []})
        else:
            self.selections.append({"function": self.Sel1_Milestone,
                            "text": "이정표가 있는 갈림길 쪽으로 이동한다.",
                            "needs": []})
                            
        self.effects = [{"name" : "setWorldValue", "key" : "is_visited_milestone_1", 'data': True}, ]

    def EnterDikeuCave(self):
        self.effects = [{"name" : "setWorldValue", "key" : "is_visited_milestone_1", 'data': True}, {"name" : "appendEvent", "value" : E_DikeuCave}]
        self.isEventCheck = True
        self.End()
        
    def RoadToPaiba(self):
        self.region = '하이델'
        self.area = '마을로 가는 길'
        self.selfDef = self.RoadToPaiba
        
        self.selections = []
        self.cells = ['1', '2', '논밭']
        self.selections = [
                           ]
        
        self.prefixDialog = [{'text' :(''), 'needs' : [], 'else' : ''}]
        self.dialog = ('§l§0 당신은 마을과 이정표 사이의 길 위에 서 있습니다. 여러 사람이 이 길을 다닌 듯, 수레바퀴 자국이 나있고 땅이 정갈합니다. '
                       '숲이나 여기나 어김없이 새가 지저귀는 소리가 들려옵니다. \n')

        self.suffixDialog = [{'text' :(''), 'needs' : [], 'else' : ''}]
        
        if(self.nowCell not in self.cells):
            self.nowCell = self.cells[0]

        if(self.nowCell != self.cells[-1]):
            self.selections.append({"function": self.CellUp,
                            "text": "파이바 마을을 향해 이동한다.",
                            "needs": []})
            self.dialog += ('§l§0 마을 쪽을 보면, 집에서 가꾸던 텃밭보다는 훨씬 큰 땅을 메우고 있는 길고 누런 풀들이 언뜻 보입니다.\n')
        else:
            self.selections.append({"function": self.EnterPaibaVillage,
                                    "text": "파이바 마을 안으로 들어간다.",
                                    "needs": []})
            self.dialog += ('§l§0 평야는 좋아보이는 땅이건만, 당신보다도 큰 쓸모없는 풀들만 자라고 있습니다. 조용히 지켜보고 있다보면 풀 속에서 §1들썩이는 소리§0가 들립니다.\n '
                            '당신은 이 땅이 방치된 이유를 알 것 같습니다.\n')
            
            
        if(self.nowCell != self.cells[0]):
            self.selections.append({"function": self.CellDown,
                            "text": "이정표가 있는 갈림길 쪽으로 이동한다.",
                            "needs": []})
        else:
            self.selections.append({"function": self.Sel1_Milestone,
                            "text": "이정표가 있는 갈림길 쪽으로 이동한다.",
                            "needs": []})
        
    def EnterPaibaVillage(self):
        self.effects = [{"name" : "setWorldValue", "key" : "is_visited_milestone_1", 'data': True}, {"name" : "appendEvent", "value" : E_PaibaVillage}]
        self.isEventCheck = True
        self.End()
        
    def RoadToBridge(self):
        self.region = '하이델'
        self.area = '다리'
        self.selfDef = self.RoadToBridge
        self.defCode = 4
        self.selections = []
        self.cells = ['앞']
        self.nowCell = ''
        self.effects = []
        self.prefixDialog = [{'text' :(''), 
                               'needs': [{"name" : "getWorldValue", "key" : "is_paiba_bridge_fixed", 'data': True}],
                               'else' : ('§l§0 다리가 무너져 있습니다. 무너진 다리 밑으로는 세찬 물줄기가 흐르고 있습니다.\n'
                                         '')}]
        self.dialog = ('§l§0 다리 건너로는 넓은 초원이 펼쳐져있습니다. 지평선 너머로 희미하게 탑과 같은 것이 보입니다.\n')
        self.selections = [{"function": self.Sel1_Milestone,
                            "text": "이정표로 돌아간다.",
                            "needs": []},]

        if(self.nowCell not in self.cells):
            self.nowCell = self.cells[0]


    
    def CellUp(self):
        self.Move(1)

    def CellDown(self):
        self.Move(-1)


    def Move(self, _vector):
        _cell_value = self.cells.index(self.nowCell)
        self.nowCell = self.cells[_cell_value + _vector]
        self.selfDef()

        
    def End(self):
        self.isEnd = True




class E_DikeuCave():
    def __init__(self):
        self.percent = 5
        self.needState = {}
        self.cell = 0
        self.eventName = '디크_동굴'

        self.area = '디크 동굴'
        self.region = '하이델'
        self.effects = [{"name":"damage", "value":"0"}]
        self.isBattle = False
        self.isEventCheck = False
        self.bgm = "eCaveWater"
        self.needState = {}
        self.dialog = ('\n')
        
        self.prefixDialog = []
        self.suffixDialog = []
        self.isEnd = False 
        #아 그냥 events에서만 쓰는 변수들 좀 만들까 아 그럼 근데 또 코드가 더럽고 좀 그래
    
        self.cells = ['1', '2', '3', '공동']
        self.nowCell = self.cells[0]

        self.callEndFuntion = self.End
        self.reset()

    def reset(self):
        self.bgm = "eCaveWater"
        self.needState = {}
        self.prefixDialog =  []
        self.effects = []
        self.suffixDialog = []
        self.isEnd = False 
        self.selections = [] 

        self.dialog = ('§l§0 당신은 동굴을 걸어가고 있습니다. 햇빛은 들지 않건만, 바닥엔 빛나는 버섯이 비추고 천장은 '
                       '기묘하게 발광하는 돌이 비춰 앞을 보는데는 큰 무리가 없습니다. '
                       '다만, 당신은 간혹 떨어지는 거미와 눅눅하다는 점에 불평합니다. \n')

        if(self.nowCell != self.cells[-1]):
            self.selections.append({"function": self.CellUp,
                                    "text": "동굴 깊숙히 들어간다",
                                    "needs": []}, )
            if(C_TorF(40)):
                self.dialog += ('\n\n§l§0 물방울이 떨어지는 소리가 귀를 간지럽힙니다.\n')
        else:
            if(player.GetWorldValue('is_win_Phantom1') == False):
                self.dialog = ('§l§0 당신은 기시감에 몸서리칩니다. 온 몸에는 소름이 돋고, 괜스레 뒤에서 바람이 불어오는 듯 합니다. '
                               '적막에 휩싸인 동굴이지만 거미와 어둠의 비명소리가 들리는 것만 같습니다. 과연 이 일을 해내면 동생을 찾을 수 있을까, 당신은 그런 생각이 듭니다.\n\n\n'
                               '§c§1...이 앞에서 불길한 기운이 넘실대고 있습니다.\n'
                               )
                self.selections.append({"function": self.EncounterPhantom,
                                        "text": "마주한다.",
                                        "needs": []}, )
            else:
                self.dialog += ('\n\n§l§0 더이상 공동에 악령은 없습니다. 다만 그가 있던 자리에 버섯이 자욱하게 퍼져났습니다.\n')

        if(self.nowCell != self.cells[0]):
            self.selections.append({"function": self.CellDown,
                                    "text": "바깥으로 걸어간다.",
                                    "needs": []}, )
        else:
            self.selections.append({"function": self.Exit,
                                    "text": "동굴 밖으로 나간다.",
                                    "needs": []}, )
            

        
        
        
        

        



        self.isBattle = False
        self.isEventCheck = False
        self.callEndFuntion = self.End

   


    def EncounterPhantom(self):
        self.dialog = ('§c§0 기운을 따라 나선 곳엔 커다란 공동이 있습니다. 공동 한 가운데에 흐릿하게 보이는 남자의 인영이 보입니다. 당신과 키가 비슷해 보입니다. '
                       '은은한 빛이 비치고 있음에도, 어둡고 흐릿해서 인영만이 보입니다. 하지만 분명 당신은 느낄 수 있습니다. 녀석도 당신을 바라보고 있습니다.\n\n\n'
                       '§c§0 이제와서 돌아가기엔 늦은 듯 합니다.\n'
                       )
        self.effects = []
        self.selections = [{"function": self.BattleStart,
                            "text": "싸움을 준비한다!",
                            "needs": []}, 
                        ]
        
        self.isEventCheck = True


    def BattleStart(self):
        self.dialog = ('§l§1\n')
        
        self.effects = [{"name" : "damage", "value" : "0"}, 
                        {"name" : "battle", "enemies": [{'enemy' : M_Phantom, 'chance' : 100}]}]
        
        self.callEndFuntion = self.BattleEnd
        self.isBattle = True
        self.isEventCheck = True
        
    def BattleEnd(self):
        self.effects = []
        self.isBattle = False
        self.EndPhantom()
        self.isEventCheck = True
        

    def EndPhantom(self):
        player.SetWorldValue('is_win_Phantom1', True)
        self.bgm = 'orgol'
        self.dialog = ('§c§0흐릿한 형체와 함께 당신을 옥죄던 압박감도 사라졌습니다. 어떤 기억이 흘러들어오고, 몸이 좀 더 성숙해진 것 같습니다. (Gain Skill!, Gain Str!)\n'
                       '§c§0당신은 그순간 어디로 가야할 지 알게 되었습니다.\n\n'
                       '§c§0다만, 당신은 이 뒤의 이야기가 아직 쓰여지지 않았음을 알고 있습니다.\n'
                       '§c§0동시에 이야기는 완성될 것임을 알고 있습니다.\n\n'
                       '§c§0언제고 새로운 이야기가 쓰여질 때까지,\n'
                       '§c§0당신은 다시금, 다시금, 주어진 이야기를 곱씹을 것 입니다.\n'
                       '§c§0언제고 새로운 이야기가 쓰여질 때까지...\n\n\n\n\n'
                       '§c§3~아직 쓰여지지 않은 이야기를 기다리며~\n'
                       )
        self.effects = []
        self.selections = [{"function": self.reset,
                            "text": "...이야기를 좀 더 곱씹는다.",
                            "needs": []}, 
                        ]
        
        self.isEventCheck = True
    def CellUp(self):
        self.Move(1)

    def CellDown(self):
        self.Move(-1)


    def Move(self, _vector):
        _cell_value = self.cells.index(self.nowCell)
        self.nowCell = self.cells[_cell_value + _vector]
        self.reset()
        

        

    def Exit(self):
        self.effects = [{'name': 'appendEvent', 'value': E_PaibaRoad}]
        self.isEventCheck = True
        self.End()
    
    def End(self):
        self.isEnd = True


class E_PaibaVillage():
    def __init__(self):
        self.percent = 5
        self.needState = {}
        self.cell = 0
        self.eventName = '파이바_마을'

        self.area = '파이바 마을'
        self.region = '하이델'
        self.effects = [{"name":"damage", "value":"0"}]
        self.isBattle = False
        self.isEventCheck = False
        self.bgm = "eForest"
        self.needState = {}
        self.dialog = ('\n')
        
        self.prefixDialog = []
        self.suffixDialog = []
        self.isEnd = False 
        #아 그냥 events에서만 쓰는 변수들 좀 만들까 아 그럼 근데 또 코드가 더럽고 좀 그래
    
        self.cells = ['마을 입구', '거리 1', '거리 2', '거리 3']
        self.nowCell = self.cells[0]

        self.callEndFuntion = self.End
        self.reset()

    def reset(self):
        self.bgm = "eForest"
        self.needState = {}
        self.dialog = ('§l§0 당신은 마을에 들어왔습니다. 마을에는 당신의 또래로 보이는 어린아이들이 뛰어다니고 있습니다. 길가에는 상인들이 가판대를 펼쳐두고 있습니다. '
                       '사람이 많이 오가지만서도 묘하게 조용합니다. 마치 그들의 삶이 덜 묘사된 것만 같습니다.\n'
                       )
        
        
        self.prefixDialog = []
        self.effects = []
        self.suffixDialog = []
        self.isEnd = False 
        self.selections = [{"function": self.TalkAnyone,
                            "text": "아무나에게 동생에 대해 묻는다.",
                            "needs": [{'name': 'getWorldValue', 'key' : 'is_talked_black_man_PaibaViliage', 'data' : False}]}, #근데...이거 그냥 저걸로도 가져올 수 있는거 아닌가 custom_operator
                           ]
        



        #거리1 - 상점들
        #NEED ADD : 상점에서 아이템 판매 및 구매




        if(self.nowCell != self.cells[-1]):
            self.selections.append({"function": self.CellUp,
                                    "text": "마을 안쪽으로 걸어간다.",
                                    "needs": []}, )
        else:
            #이말 == '아직 안 만들었다~'
            self.dialog += ('\n\n§l§0마을의 끝에 도착했습니다. 정말... 끝인 것 같습니다. 아무것도 없습니다. 이 앞은 아직 쓰여지지 않은 듯 합니다.\n')
        

        if(self.nowCell != self.cells[0]):
            self.selections.append({"function": self.CellDown,
                                    "text": "마을 밖 쪽으로 걸어간다",
                                    "needs": []}, )
        else:
            self.prefixDialog =  [{'text': ('§l§0 ' 
                                        '처음보는 타인에 당신의 마음이 설레입니다. '  
                                        '한편으론 동생이 이 마을에 있을까 하는 생각이 듭니다. \n'), 
                             'needs': [{'name': 'getWorldValue', 'key' : 'VisitedPaibaVillage', 'data' : False}], 
                             'else': ('\n')
                             }]
            self.selections.append({"function": self.Exit,
                                    "text": "마을을 나간다",
                                    "needs": []}, )
        
        

        



        self.isBattle = False
        self.isEventCheck = False
        self.callEndFuntion = self.End

    def TalkAnyone(self):
        self.dialog = ('§l§0당신은 동생의 행방을 물어볼 사람을 물색합니다. 멈춘 시선 끝에는 왠지 험악하면서도 친절해보이는 건장한 체격의 남성이 서있습니다. '
                       '검은 복장을 하고 있는데, 꼭 당신이 책에서 봤던 사제의 모습을 닮았습니다. 그가 시선을 눈치채곤 다가옵니다. \n'
                       '§l§0"그댄 운명을 믿소?"\n'
                       '당신은 말을 이해하지 못했습니다. 다만 동생을 찾고 있다고 이야기 하니 이어서 말합니다. \n'
                       '"운명적 만남이란 말이 있지... 지금이 그런 것 같소. 내가 그대에게 길을 인도해줄 자를 알고있소. 따라오겠소?"\n'
                       '굉장히, 상당히 괴짜같아보이는 사람입니다. 하지만 언행이 얼굴과 묘하게 어울려서 믿음직해 보이기도 합니다. \n'
                       )
        self.prefixDialog = []
        self.suffixDialog = []
        self.effects = [{"name" : "setWorldValue", "key" : "is_talked_black_man_PaibaViliage", 'data': True}, ]
        self.selections = [{"function": self.FollowMan,
                            "text": "따라간다.",
                            "needs": []},
                            {"function": self.RejectMan,
                            "text": "정중히 거절한다.",
                            "needs": []},

                           ]
                           
        
        self.isEventCheck = True


    def RejectMan(self):
        self.dialog = ('§l§0당신은 그의 말을 거절했습니다\n\n '
                       '§c§0"상식에 사로잡히지 마..."\n\n'
                       '§l§0남자가 낮게 읊조린 말이 귓가를 맴돕니다. 당신은 고개를 흔들어 털어버리고 다시 동생을 찾고자 발길을 제촉합니다. \n'
                       )
        self.prefixDialog = []
        self.suffixDialog = []
        self.effects = []
        self.selections = [{"function": self.reset,
                            "text": "떠난다.",
                            "needs": []},
                           ]
        
        self.isEventCheck = True

    def FollowMan(self):
        self.dialog = ('§l§0 그는 느끼한 미소를 짓고 당신을 인도합니다. 길을 걸어가다 골목으로 들어갑니다. '
                       '골목으로 들어가자 밖에선 보이지 않던 숨겨진 제단이 몸을 드러냅니다. '
                       '제단에는 무어라 할 수 없는, 난생 처음보는 검은 기운이 일렁거리고 있습니다. 그럼에도 당신은 굉장히 익숙한 듯한 느낌을 느낍니다. '
                       '제단의 가운데에는 여성 형체의 조각상이 서있습니다. 이것이 괴이한 아우라의 근원지인 것 같습니다.\n'
                       '"§q고귀한 어둠§0께서 그대가 어디로 가야할 지 알고 있을 것이오."\n'
                       )
        self.selections = [{"function": self.FollowMan_1,
                            "text": "여동생의 행방을 묻는다.",
                            "needs": []},
                           ]
    def FollowMan_1(self):
        self.dialog = ('§c§0"§5아이야, 천치인 아이야, 내가 친히 네게 길을 알려주도록 하마. 다만 이로 하여금 너와 나는 길고 긴 연이 닿겠구나.§0"\n'
                       '§c§0"§5아이야, 아이야. 네 동생을 찾고 싶다면 한참은 먼 길을 가야한다...§0"\n'
                       '§c§0"§5그 첫 걸음은 디크 동굴이 되겠구나.§0"\n'
                       '§c§0"§5디크 동굴의 악령을 쓰러뜨려라.§0"\n'
                       '§c§0"§5다만 네 힘이 미약하니, 내 작은 선물을 내려주마§0"\n\n\n'
                       '§l§0굉장히 희미한 목소리지만 뚜렷하게 들리는 목소리입니다.\n'
                       '§c§3당신의 몸에 신비한 힘이 깃듭니다. 힘이 세진 것 같습니다.\n'
                       )
        self.effects = [{'name' : 'modifyState', 'value' : 'str', 'amount' : 6}, {'name' : 'modifyState', 'value' : 'str', 'amount' : 6},]
        self.selections = [{"function": self.reset,
                            "text": "떠난다.",
                            "needs": []},
                           ]
        self.isEventCheck = True
    def CellUp(self):
        self.Move(1)

    def CellDown(self):
        self.Move(-1)


    def Move(self, _vector):
        _cell_value = self.cells.index(self.nowCell)
        self.nowCell = self.cells[_cell_value + _vector]
        self.reset()


        

    def Sel2_BattleStart(self):
        self.dialog = ('§l§1\n')
        
        self.effects = [{"name" : "damage", "value" : "0"}, 
                        {"name" : "battle", "enemies": [{'enemy' : M_PariahDog, 'chance' : 100}]}]
        
        self.callEndFuntion = self.Sel2_BattleEnd
        self.isBattle = True
        self.isEventCheck = True
        
    def Sel2_BattleEnd(self):
        self.effects = []
        self.reset()
        
        self.isBattle = False
        self.isEventCheck = True
        

    def Exit(self):
        self.effects = [{'name': 'appendEvent', 'value': E_PaibaRoad}, 
                        {'name': 'setWorldValue', 'key' : 'VisitedPaibaVillage', 'data' : True}] 
        self.isEventCheck = True
        self.End()
    
    def End(self):
        self.isEnd = True