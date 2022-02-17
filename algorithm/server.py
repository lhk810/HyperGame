from fastapi import FastAPI
from starlette.responses import JSONResponse

import domain
import random_decision

app = FastAPI(debug=True)

player_name = "hk"

@app.post("/decide")
def decide(request: domain.Input):
    print(request)
    state = dict(request)['state']
    if state.player != player_name:
        error = {'status':'INTERNAL SERVER ERROR'}
        return JSONResponse(error)
    decided = random_decision.random_decision(state.dices, state.scoreBoard.__root__[player_name]) #check later
    response = {'decision':{'choice':decided}}
    return JSONResponse(response)
