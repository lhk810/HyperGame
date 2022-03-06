import random

from typing import List

import domain
import util

def decision_policy(dices: List[int], dices_scores: dict, current_score: domain.Score, trial):
    expected = {}

    if dices_scores["yacht"] > 0 and getattr(current_score, "yacht") is not None:
        return {'choice' : 'yacht'}

    cnt_list = util.cnt_list
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
        if max(cnt_list) > 1 and trial < 3:
            keep = [idx for idx, item in enumerate(dices) if item == cnt_list.index(max(cnt_list))]
            return {'keep' : keep}
        if max(cnt_list) > 3 and trial == 3:
            if cnt_list.index(max(cnt_list)) == 1:
                return {'choice' : 'aces'}
            if cnt_list.index(max(cnt_list)) == 2:
                return {'choice' : 'deuces'}
            if cnt_list.index(max(cnt_list)) == 3:
                return {'choice' : 'threes'}
            if cnt_list.index(max(cnt_list)) == 4:
                return {'choice' : 'fours'}
            if cnt_list.index(max(cnt_list)) == 5:
                return {'choice' : 'fives'}
            if cnt_list.index(max(cnt_list)) == 6:
                return {'choice' : 'sixes'}

    ordered_scores = sorted(dices_scores.items(), key=(lambda x : x[1]), reverse=True)
    for i in range(len(ordered_scores)):
        item = ordered_scores[i][0]
        if getattr(current_score, item) is None:
            return {'choice' : item}

def rule_based_decision(dices: List[int], score: domain.Score, trial: int):
    util.update_cnt_list(dices)
    dices_scores = util.score_map(dices)
    
    return decision_policy(dices, dices_scores, score, trial)
