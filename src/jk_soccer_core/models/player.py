from dataclasses import dataclass


@dataclass
class Player:
    name: str
    position: str = None
    number: int = None
