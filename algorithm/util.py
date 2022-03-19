from typing import List

import domain

cnt_list = []
accumulated = [0,0,0,0,0,0,0]
names = ['', 'aces', 'deuces', 'threes', 'fours','fives', 'sixes']

def update_info(dices: List[int], score: domain.Score):
    global cnt_list
    cnt_list = []
    for i in range(0,7):
        cnt = dices.count(i)
        cnt_list.append(cnt)

    global accumulated
    accumulated = [0,0,0,0,0,0,0]
    for i in range(1,7):
        accumulated[i] = accumulated[i-1] + 1 if i in dices else 0

    global current_score
    current_score = score

def choosable_list(current_score: domain.Score):
    ret = []
    for item in current_score:
        if item[1] is None:
            ret.append(item[0])
    return ret

def score_map(dices : List[int])->dict:
    ret = {}

    global cnt_list
    for i in range(1,7):
        ret[names[i]] = cnt_list[i]*i

    ret["fullHouse"] = cnt_list.index(2)*2 + cnt_list.index(3)*3 if 2 in cnt_list and 3 in cnt_list else 0
    ret["fourKind"] = sum(cnt_list) if max(cnt_list) >= 4 else 0
    ret["yacht"] = 0
    if 5 in cnt_list:
        ret["yacht"] = 50
        ret["fullHouse"] = cnt_list.index(5)*5

    global accumulated
    ret["smallStraight"] = 15 if 4 in accumulated else 0
    ret["largeStraight"] = 30 if 5 in accumulated else 0

    ret["choice"] = sum(cnt_list)
    
    return ret
