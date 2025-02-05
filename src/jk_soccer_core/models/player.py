from dataclasses import dataclass


@dataclass
class Player:
    name: str
    position: str = None
    number: int = None


if __name__ == "__main__":
    player = Player("John Doe")
    print(player)
