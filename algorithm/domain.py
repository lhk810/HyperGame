from pydantic import BaseModel
from typing import Dict, List, Optional

class Score(BaseModel):
    aces : Optional[int]
    deuces : Optional[int]
    threes : Optional[int]
    fours : Optional[int]
    fives : Optional[int]
    sixes : Optional[int]
    choice : Optional[int]
    fourKind : Optional[int]
    fullHouse : Optional[int]
    smallStraight : Optional[int]
    largeStraight : Optional[int]
    yacht: Optional[int]
    total: Optional[int]

class ScoreBoardCreate(BaseModel):
    __root__ : Dict[str, Score]

class PlayerScore(BaseModel):
    hk : Score

class State(BaseModel):
    turn : int
    player : str
    trial : int
    dices : List[int]
    scoreBoard : ScoreBoardCreate

class Input(BaseModel):
    state: State
