import random
from random import randrange

INF = 2**23-1
#generating formulas... prefix is "M"... is short of 'Math'..!
#
def M_root(_formula = [32,'+',32], _value = 64):
    '''
    ONLY INPUT SQUARE NUMBE!!!!!
    ex) 64, 4, 16, 9.. -> 16, 2, 4, 3
    this function draw Root.
    '''
    _formula.insert(0, 'root')
    _formula.append('rootend')
    return _formula, int(_value**(0.5))



def M_add(_level = 1, _count = 2, _mode = 0, _fixResult = INF):  
    '''
    level : difficult(= number range... 10**level) 
    count : number stack
    mode : only plus(1), only minus(-1), both(0)
    '''
    #return... formula array, and result value
    if(_fixResult == INF):
        _value = 0
        _formula = []
        for i in range(_count):
            _random_number = randrange(-10**_level, 10**_level)
            if(_mode == 1):
                _random_number = abs(_random_number)
            elif(_mode == -1):
                _random_number = -abs(_random_number)
            _value += _random_number
            _formula.append(_random_number)
            _formula.append('+')
        del _formula[-1]
    else:
        _value = 0
        _formula = []
        for i in range(_count-1):
            _random_number = randrange(-10**_level, 10**_level)
            if(_mode == 1):
                _random_number = abs(_random_number)
            elif(_mode == -1):
                _random_number = -abs(_random_number)
            _value += _random_number
            _formula.append(_random_number)
            _formula.append('+')
        _formula.append(_fixResult - _value)
        _value = _fixResult
    
    return _formula, _value


def M_sort():
    '''
    this function try to [1, '+', -1] -> [1, '-', 1]
    try at last.
    '''
    print()
def M_merge():
    '''
    this function try to [1, '-', 1] -> [1, '+', -1]
    '''
    print() 