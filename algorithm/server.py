from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse
from typing import List

app = FastAPI()

class Score(BaseModel):
    aces : int
    decues : int
    threes : int
    fours : int
    fives : int
    sixes : int
    choice : int
    fourKind : int
    fullHouse : int
    smallStraight : int
    largeStraight : int
    yacht: int

class Player(BaseModel):
    name : str
    score : Score

class State(BaseModel):
    turn : int
    player : str
    trial : int
    dices : List[int]
    scoreBoard : List[Player]

class History(BaseModel):
    states : List[State]

@app.get("/history")
def get_history():
    state = []
    # fetch previous desicions here
    return JSONResponse(state)
