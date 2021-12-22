import pytest

# from player import get_actions, get_player_info
from models import ActionRequest, Action, Mark, GameState, PlayerRegistration
from player.player import get_actions, get_player_info


@pytest.fixture
def action_request():
    game_state = GameState(board=[[Mark.NONE for _ in range(0,3)] for __ in range(0,3)])
    return ActionRequest(state=game_state, player_mark=Mark.CIRCLE)

def test_get_actions_returning_list(action_request):
    actions = get_actions(action_request)
    assert isinstance(actions, list)

def test_get_actions_returning_list_of_actions(action_request):
    actions = get_actions(action_request)
    assert all(isinstance(a, Action) for a in actions)

def test_player_registration():
    player_info = get_player_info()
    assert isinstance(player_info, PlayerRegistration)