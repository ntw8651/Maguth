import random




#C is Custom
def C_Lerp(a, b, p):
    return a * p + b * (1-p)

#확률계산
def C_TorF(a = 50):
    '''
    확률적으로 True나 False를 반환함. 소숫점 2자리까지 적용됨.
    a: True가 나올 확률(0~100)
    '''
    _Choice = random.randrange(1, 10001, 1)
    _Choice*=0.01
    if(_Choice <= a):
        return True
    
    return False

C_V_times = {}
def C_DelayClear(_state = 'all'):
    global C_V_times
    if(_state == 'all'):
        C_V_times = {}
    elif(_state == 'battle'):
        if('BattleEnd' in C_V_times.keys()):
            del C_V_times['BattleEnd']


def C_GetDelay(_name, _now_time):
    '''
    딜레이에 관한 정보 반환해 줌. 
    oppacity, position 조정 등에 사용

    length : 길이
    time : 지난 시간
    *참고) 다 tick단위라 TICK_PER_SEC를 곱해줄 것
    '''
    return {'time' : _now_time - C_V_times[_name], 'length' : C_V_times}

def C_Delay(_name, _now_time, _time_length):
    '''
    _name : 이름 기억용
    _now_time : 현재시간(tick_count 넣어주면 됨)
    _time_length : 대기 프레임(TICK_PER_SEC 곱해줄 것))
    '''
    if(_name in C_V_times.keys()):
        if(_now_time - C_V_times[_name] > _time_length):
            del C_V_times[_name]
            return True
        else:
            return False
    else:
        C_V_times[_name] = _now_time
        return False
    
inputs_pressed = {}

def C_PressKey(_key, _is_pressed = True):
    global inputs_pressed
    inputs_pressed[_key] = _is_pressed

def C_PressedKeyCheck(_key):
    global inputs_pressed
    if(_key in inputs_pressed):
        return inputs_pressed[_key]
    else:
        inputs_pressed[_key] = False
        return False
