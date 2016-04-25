# coding: utf-8
import sys

# закодируем правила в виде кортежа (состояние, вход, новое_состояние, выход, перемещение)
# при каждой смене состояния выводить состояние автомата
# Если новое_состояние STOP, то вывести состояние и остановиться

if len(sys.argv) <3:
    print('usage:', sys.argv[0], ' rules-file init-file')
else:
    fname_1 = sys.argv[1]
    fname_2 = sys.argv[2]
    
    rules = {}
    tape = []
    
    with open(fname_1, 'r') as file1:
        s = file1.readline().rstrip()
        while s:
            if s[0:2] != '//':
                (_in, _state, _out, _new_state, _dir) = s.split(',')
                if _in not in rules:
                    rules[_in] = {}
                rules[_in][_state] =  (_out, _new_state, _dir) 
            s = file1.readline().strip()
    
    with open(fname_2, 'r') as file2:
        _state = file2.readline().strip() 
        s = file2.readline().strip()
        while s:
            tape.append(s)
            s = file2.readline().strip()
    
    print(*tape)
    
    _pointer = 0
    while _state != 'STOP':
        _in = tape[_pointer]
        if _state not in rules[_in]: # недопустимое состояние - завершим цикл
            _state = 'STOP'
        else:
            (_out, _new_state, _dir) = rules[_in][_state]
            if _new_state != 'STOP':
                tape[_pointer] = _out
                if _dir == 'R':
                    _pointer += 1
                    if _pointer>=len(tape):
                        tape.append('B')
                elif _dir == 'L':
                    _pointer -= 1
                    if _pointer < 0:
                        tape.insert(0,'B')
                        _pointer = 0
    
            _state = _new_state
    
    print(*tape)
    