import random

from typing import List

import domain

def possible(dices: List[int], score: domain.Score):
    ret = set()
    if 1 in dices:
        ret.add("aces")
    if 2 in dices:
        ret.add("deuces")
    if 3 in dices:
        ret.add("threes")
    if 4 in dices:
        ret.add("fours")
    if 5 in dices:
        ret.add("fives")
    if 6 in dices:
        ret.add("sixes")
    
    cnt_list = []
    for i in range(1,7):
        cnt = dices.count(i)
        cnt_list.append(cnt)
    if 2 in cnt_list and 3 in cnt_list:
        ret.add("fullHouse")
    if 4 in cnt_list:
        ret.add("fourKind")
    if 5 in cnt_list:
        ret.add("yacht")
    
    accumulated = [0,0,0,0,0,0,0]
    for i in range(1,7):
        accumulated[i] = accumulated[i-1] + 1 if i in dices else 0
    if 4 in accumulated:
        ret.add("smallStraight")
    if 5 in accumulated:
        ret.add("largeStraight")

    # filter already checked
    ret_filtered = set(ret)
    for item in ret:
        if getattr(score, item):
            ret_filtered.discard(item)

    # choose any if set is empty
    if len(ret_filtered) == 0:
        members = score.__dict__.keys()
        members = [item for item in members if not getattr(score, item)]
        return set(members)

    return ret_filtered

def random_decision(dices: List[int], score: domain.Score):
    possible_choices = possible(dices, score)
    return random.choice(list(possible_choices))
