import random

from typing import List

import domain
import util

def decision_policy(dices: List[int], dices_scores: dict, current_score: domain.Score, trial):
    expected = {}

    cnt_list = util.cnt_list
    accumulated = util.accumulated
    names = util.names
    if dices_scores["yacht"] > 0 and getattr(current_score, "yacht") is None:
        return {'choice' : 'yacht'}

    if getattr(current_score, 'largeStraight') is None and max(util.accumulated) == 4 and trial < 3:
        max_val = accumulated.index(4)
        keep = []
        for i in range(max_val, max_val - 4, -1):
            keep.append(dices.index(i))
        return {'keep' : keep}

    if dices_scores["fullHouse"] > 15 and getattr(current_score, 'fullHouse') is None:
        return {'choice' : 'fullHouse'}

    subtotal = 0
    subtotal += getattr(current_score, "aces") if getattr(current_score, "aces") else 0
    subtotal += getattr(current_score, "deuces") if getattr(current_score, "deuces") else 0
    subtotal += getattr(current_score, "threes") if getattr(current_score, "threes") else 0
    subtotal += getattr(current_score, "fours") if getattr(current_score, "fours") else 0
    subtotal += getattr(current_score, "fives") if getattr(current_score, "fives") else 0
    subtotal += getattr(current_score, "sixes") if getattr(current_score, "sixes") else 0

    go_for_subtotal = True \
        if None in [getattr(current_score, "aces"), getattr(current_score, "deuces"), getattr(current_score, "threes"), \
                    getattr(current_score, "fours"), getattr(current_score, "fives"), getattr(current_score, "sixes")] \
        else False
    if go_for_subtotal and subtotal < 63:
        max_val = 0
        max_cnt = 0
        for val, cnt in enumerate(cnt_list):
            if cnt > max_cnt and getattr(current_score, names[val]) is None:
                max_val = val
                max_cnt = cnt
            if cnt == max_cnt and val > max_val and getattr(current_score, names[val]) is None:
                max_val = val
        if trial < 3:
            keep = [idx for idx, item in enumerate(dices) if item == max_val]
            return {'keep' : keep}
        if trial == 3 and max_cnt > 2:
            if max_val > 4 and max_cnt == 3 and getattr(current_score, 'choice') is None:
                return {'choice' : 'choice'}
            return {'choice' : util.names[max_val]}

    if getattr(current_score, 'smallStraight') is None and max(util.accumulated) == 3 and trial < 3:
        max_val = accumulated.index(3)
        keep = []
        for i in range(max_val, max_val-3, -1):
            keep.append(dices.index(i))
        return {'keep' : keep}

    ordered_scores = sorted(dices_scores.items(), key=(lambda x : x[1]), reverse=True)
    for i in range(len(ordered_scores)):
        item = ordered_scores[i][0]
        if getattr(current_score, item) is None:
            return {'choice' : item}

def rule_based_decision(dices: List[int], score: domain.Score, trial: int):
    util.update_cnt_list(dices)
    util.update_accumulated(dices)
    dices_scores = util.score_map(dices)
    
    return decision_policy(dices, dices_scores, score, trial)
