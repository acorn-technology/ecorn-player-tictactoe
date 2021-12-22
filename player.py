import random
from typing import List

from models import Action, ActionRequest, Mark

# Player controll logic
def get_actions(action_request: ActionRequest) -> List[Action]:
    possible = []
    for y, row in enumerate(action_request.state.board):
      for x, mark in enumerate(row):
            if mark == Mark.NONE:
                possible.append(Action(x=x, y=y))
            
    if possible:
        return [random.choice(possible)]
    else:
        return []
  

def get_player_info():
  return {
    "id": "cc9ddc91-2e0d-4565-af30-a39748f2344b",
    "name": "Swamp prawns"
  }
