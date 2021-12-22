from models import Action, ActionRequest, Mark

# Player controll logic
def get_actions(state: ActionRequest):
  for y in range(0, 3):
    for x in range(0, 3):
        if state.state.board[y][x] == Mark.NONE:
            return [Action(x=x, y=y)]

  return []

def get_player_info():
  return {
    "id": "cc9ddc91-2e0d-4565-af30-a39748f2344b",
    "name": "Swamp prawns"
  }
