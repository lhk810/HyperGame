from fastapi import FastAPI
from starlette.responses import JSONResponse

import domain
import rule_base

app = FastAPI(debug=True)

player_name = "hk"

@app.post("/decide")
def decide(request: domain.Input):
    print(request)
    state = dict(request)['state']
    if state.player != player_name:
        error = {'status':'INTERNAL SERVER ERROR'}
        return JSONResponse(error)
    #decided = rule_base.rule_base(state.dices, state.scoreBoard.__root__[player_name]) #check later
    decided = rule_base.rule_based_decision(state.dices, state.scoreBoard.__root__[player_name])
    print(f"the decision is {decided}")
    response = {'decision':decided}
    return JSONResponse(response)
