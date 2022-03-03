from typing import List

import domain

def score_map(dices : List[int])->dict:
    ret = {}

    cnt_list = []
    for i in range(0,7):
        cnt = dices.count(i)
        cnt_list.append(cnt)

    ret["aces"] = cnt_list[1]*1
    ret["deuces"] = cnt_list[2]*2
    ret["threes"] = cnt_list[3]*3
    ret["fours"] = cnt_list[4]*4
    ret["fives"] = cnt_list[5]*5
    ret["sixes"] = cnt_list[6]*6

    ret["fullHouse"] = cnt_list.index(2)*2 + cnt_list.index(3)*3 if 2 in cnt_list and 3 in cnt_list else 0
    ret["fourKind"] = cnt_list.index(4)*4 if 4 in cnt_list else 0
    ret["yacht"] = 50 if 5 in cnt_list else 0

    accumulated = [0,0,0,0,0,0,0]
    for i in range(1,7):
        accumulated[i] = accumulated[i-1] + 1 if i in dices else 0
    ret["smallStraight"] = 15 if 4 in accumulated else 0
    ret["largeStraight"] = 30 if 4 in accumulated else 0

    ret["choice"] = sum(cnt_list)
    
    return ret
