from typing import List
from .thing import Thing
from .player import Player
from .coach import Coach


class Team(Thing):
    players: List[Player]
    coaches: List[Coach]
