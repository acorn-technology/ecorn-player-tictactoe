from typing import List
from pydantic import BaseModel, UUID4
from enum import IntEnum, auto, unique

class PlayerRegistration(BaseModel):
    id: UUID4
    name: str

@unique
class Mark(IntEnum):
    NONE = auto()
    CIRCLE = auto()
    CROSS = auto()

class Action(BaseModel):
    x: int
    y: int

class GameState(BaseModel):
    board: List[List[Mark]]

class ActionRequest(BaseModel):
    player_mark: Mark
    state: GameState