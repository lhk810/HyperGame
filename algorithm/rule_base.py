import random

from typing import List

import domain
import util

def rule_based_decision(dices: List[int], score: domain.Score):
    dices_scores = util.score_map(dices)
    ordered_scores = sorted(dices_scores.items(), key=(lambda x : x[1]), reverse=True)
    for i in range(len(ordered_scores)):
        item = ordered_scores[i][0]
        if getattr(score, item) is None:
            return {'choice' : item}
