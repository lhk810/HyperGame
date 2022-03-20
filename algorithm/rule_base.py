import random

from typing import List

import domain
import util

def is_choosable(name: str):
    return getattr(util.current_score, name) is None

def decision_policy(dices: List[int], dices_scores: dict, current_score: domain.Score, trial):
    cnt_list = util.cnt_list
    accumulated = util.accumulated
    names = util.names
    current_score = util.current_score

    # try yacht
    if dices_scores["yacht"] > 0 and is_choosable('yacht'):
        return {'choice' : 'yacht'}
    if max(cnt_list) >= 2 + trial and is_choosable('yacht'):
        print('keep for yacht')
        return {'keep' : [idx for idx, item in enumerate(dices) if item == cnt_list.index(max(cnt_list))]}

    # try largeStraight
    if is_choosable('largeStraight') and max(accumulated) == 5:
        return {'choice' : 'largeStraight'}
    if is_choosable('largeStraight'):
        keep = []
        if max(accumulated) == 4 and ((getattr(current_score, 'smallStraight') is None and trial < 3) or trial == 1):
            print('keep for largeStraight case1')
            max_val = accumulated.index(4)
            for i in range(max_val, max_val - 4, -1):
                keep.append(dices.index(i))
            return {'keep' : keep}
        straight1 = [1,2,3,4,5]
        straight2 = [2,3,4,5,6]
        intersection1 = list(set(straight1) & set(dices))
        intersection2 = list(set(straight2) & set(dices))
        if (len(intersection1) > 3 or len(intersection2) > 3) and trial == 1:
            print('keep for largeStraight case2')
            dice_set = set()
            for i in range(1,7):
                if cnt_list[i] != 0 and accumulated[i] != 0 and i in dices:
                    keep.append(dices.index(i))
                    dice_set.add(i)
                if len(dice_set) == 4:
                    break
            return {'keep' : keep}

    # try smallStraight (1)
    if is_choosable('smallStraight') and max(accumulated) == 4:
        return {'choice' : 'smallStraight'}
    if is_choosable('smallStraight') and max(accumulated) == 3 and cnt_list[4] < 2 and cnt_list[5] < 2 and cnt_list[6] < 2 and trial == 1:
        max_val = accumulated.index(3)
        keep = []
        print('keep for smallStraight (1)')
        for i in range(max_val, max_val-3, -1):
            keep.append(dices.index(i))
        return {'keep' : keep}

    # check fourKind
    if dices_scores['fourKind'] > 0  and is_choosable('fourKind') and ((not is_choosable(names[max(cnt_list)]) and max(cnt_list) > 3) or max(cnt_list) <= 3):
        return {'choice' : 'fourKind'}

    # check subtotal
    subtotal = 0
    for i in range(1,7):
        subtotal += getattr(current_score, names[i]) if getattr(current_score, names[i]) else 0

    go_for_subtotal = True if None in [getattr(current_score, names[i]) for i in range(1,7)] else False

    # try fullHouse
    if dices_scores['fullHouse'] > 0  and not is_choosable(names[max(cnt_list)]) and is_choosable('fullHouse'):
        return {'choice' : 'fullHouse'}

    # try subtotal
    if go_for_subtotal and subtotal < 63:
        max_val = 0
        max_cnt = 0
        for val, cnt in enumerate(cnt_list):
            if val == 1:
                continue
            if cnt > max_cnt and is_choosable(names[val]):
                max_val = val
                max_cnt = cnt
            if cnt == max_cnt and val > max_val and is_choosable(names[val]):
                max_val = val
        if trial < 3:
            print(f'keep for subtotal : {max_val}')
            keep = [idx for idx, item in enumerate(dices) if item == max_val]
            return {'keep' : keep}
        if trial == 3 and max_cnt > 0:
            if subtotal + sum(dices) >= 63:
                return {'choice' : names[max_val]}
            remain = 63 - subtotal
            denom = 0
            for i in range(1,7):
                if is_choosable(names[i]):
                    denom += i
            need = float(remain)/denom if denom > 0 else 0
            print(f'need is {need}, max_cnt is {max_cnt}')
            if (max_val > 4 and max_val*max_cnt < 15) or (max_val <=4 and max_cnt < need and denom < 21):
                if is_choosable('choice') and sum(dices) > 20:
                    return {'choice' : 'choice'}
                if is_choosable('aces') and is_choosable('deuces'):
                    discard_list = [dices_scores['aces'], dices_scores['deuces']]
                    print(discard_list)
                    idx = discard_list.index(max(discard_list))+1
                    return {'choice' : names[idx]}
                if is_choosable('aces'):
                    return {'choice' : 'aces'}
                if is_choosable('deuces'):
                    return {'choice' : 'deuces'}
                if is_choosable('yacht'):
                    return {'choice' : 'yacht'}
            return {'choice' : names[max_val]}

    # try straights (2)
    if (is_choosable('smallStraight') or is_choosable('largeStraight')) and max(accumulated) > 2 and trial < 3:
        max_val = accumulated.index(max(accumulated))
        keep = []
        print('keep for straights (2)')
        for i in range(max_val, max_val-max(accumulated), -1):
            keep.append(dices.index(i))
        return {'keep' : keep}

    # try fullHouse (2)
    if is_choosable('fullHouse'):
        if dices_scores['fullHouse'] > 0 and trial == 3:
            return {'choice' : 'fullHouse'}
        if max(cnt_list) > 1 and max(cnt_list) < 4 and trial < 3:
            keep = []
            print('keep for fullHouse')
            for idx, item in enumerate(dices):
                if cnt_list[item] > 1:
                    keep.append(idx)
            return {'keep' : keep}

    # try fourKind
    if is_choosable('fourKind'):
        if dices_scores['fourKind'] > 0:
            return {'choice' : 'fourKind'}
        if max(cnt_list) > 1 and trial < 3:
            max_val = 0
            max_cnt = 0
            print('keep for fourKind')
            for val, cnt in enumerate(cnt_list):
                if cnt > max_cnt:
                    max_val = val
                    max_cnt = cnt
                if cnt == max_cnt and val > max_val:
                    max_val = val
            return {'keep' : [idx for idx, item in enumerate(dices) if item == max_val]}

    # try subtotal or choose
    ordered_scores = sorted(dices_scores.items(), key=(lambda x : x[1]), reverse=True)
    for i in range(len(ordered_scores)):
        item = ordered_scores[i][0]
        score = ordered_scores[i][1]
        if go_for_subtotal and item in ['fives', 'sixes']:
            continue
        if is_choosable(item) and score > 0:
            return {'choice' : item}

    # final
    if trial < 3:
        choosable_list = util.choosable_list(current_score)
        if 'smallStraight' in choosable_list or 'largeStraight' in choosable_list:
            max_val = accumulated.index(max(accumulated))
            keep = []
            for i in range(max_val, max_val-max(accumulated), -1):
                keep.append(dices.index(i))
            return {'keep' : keep}
        else:
            for i in range(1,7):
                item = names[i]
                if item in choosable_list:
                    return {'keep' : [idx for idx, item in enumerate(dices) if item == max_val]}
            max_val = 0
            max_cnt = 0
            for val, cnt in enumerate(cnt_list):
                if cnt > max_cnt:
                    max_val = val
                    max_cnt = cnt
                if cnt == max_cnt and val > max_val:
                    max_val = val
            return {'keep' : [idx for idx, item in enumerate(dices) if item == max_val]}
    for i in range(len(ordered_scores)):
        item = ordered_scores[i][0]
        if is_choosable(item):
            return {'choice' : item}

def rule_based_decision(dices: List[int], score: domain.Score, trial: int):
    util.update_info(dices, score)
    dices_scores = util.score_map(dices)
    
    return decision_policy(dices, dices_scores, score, trial)
