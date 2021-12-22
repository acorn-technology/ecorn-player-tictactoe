import os
from types import ModuleType
import importlib
import importlib.util

import uvicorn
import fastapi

from models import ActionRequest

app = fastapi.FastAPI()

player: ModuleType = None

player_path = os.path.join(os.path.dirname(__file__), 'player/player.py')


def load_player():
    global player
    player_spec = importlib.util.spec_from_file_location('player', player_path)
    player = importlib.util.module_from_spec(player_spec)
    player_spec.loader.exec_module(player)


@app.on_event("startup")
async def startup_event():
    load_player()


@app.post('/')
def action_request_handler(action_request: ActionRequest):
    actions = player.get_actions(action_request)
    return actions


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=9080, reload=True)