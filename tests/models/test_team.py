from jk_soccer_core.models import Team, Coach, Player


def test_default_team() -> None:
    # Arrange

    # Act
    team = Team()

    # Assert
    assert len(team.__dict__) == 4, (
        f"Expected 4 attributes, but got {len(team.__dict__)}"
    )
    assert team.name is None, f"Expected None, but got {team.name}"
    assert team.description is None, f"Expected None, but got {team.description}"
    assert team.coaches is None, f"Expected None, but got {team.coaches}"
    assert team.players is None, f"Expected None, but got {team.players}"


def test_valid_team() -> None:
    # Arrange
    name = "The A Team"
    description = "The best team ever"
    coaches = [Coach(name="John"), Coach(name="Jane")]
    players = [Player(name="Alice"), Player(name="Bob")]

    # Act
    team = Team(name=name, description=description, coaches=coaches, players=players)

    # Assert
    assert team.name == name, f"Expected {name}, but got {team.name}"
    assert team.description == description, (
        f"Expected {description}, but got {team.description}"
    )
    assert team.coaches == coaches, f"Expected {coaches}, but got {team.coaches}"
    assert team.players == players, f"Expected {players}, but got {team.players}"
