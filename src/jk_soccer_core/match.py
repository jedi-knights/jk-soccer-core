from collections.abc import Iterable

from .models import Match


class MatchDecorator:
    """
    Decorator for the Match model
    """

    def __init__(self, match: Match):
        self.__match = match

    @property
    def match(self) -> Match:
        """
        Get the match
        """
        return self.__match

    @property
    def is_draw(self) -> bool:
        """
        Check if the match is a draw
        """
        return self.__match.home_score == self.__match.away_score

    @property
    def winner(self) -> str | None:
        """
        Get the winning team
        """
        if self.__match.home_score > self.__match.away_score:
            return self.__match.home_team

        if self.__match.away_score > self.__match.home_score:
            return self.__match.away_team

        return None

    @property
    def loser(self) -> str | None:
        """
        Get the losing team
        """
        if self.__match.home_score < self.__match.away_score:
            return self.__match.home_team

        if self.__match.away_score < self.__match.home_score:
            return self.__match.away_team

        return None

    def won(self, team_name: str | None) -> bool:
        """
        Check if the team won the match
        """
        if team_name is None:
            return False

        return self.winner == team_name

    def lost(self, team_name: str | None) -> bool:
        """
        Check if the team lost the match
        """
        if team_name is None:
            return False

        return self.loser == team_name

    def has_team_name(self, team_name: str | None) -> bool:
        """
        Check if the match contains a specific team name
        """
        return (
            self.__match.home_team == team_name or self.__match.away_team == team_name
        )

    def get_opponent_name(self, target_team_name: str) -> str | None:
        """
        Get the name of the opponent of a specific team
        """
        if not self.has_team_name(target_team_name):
            return None

        return (
            self.__match.home_team
            if self.__match.away_team == target_team_name
            else self.__match.away_team
        )


def get_team_names(matches: Iterable[Match]) -> list[str]:
    """
    Get the unique non-None team names that appear in any of the matches.
    Order is the order each name first appears.
    """
    seen: dict[str, None] = {}
    for match in matches:
        if match.home_team is not None:
            seen.setdefault(match.home_team)
        if match.away_team is not None:
            seen.setdefault(match.away_team)
    return list(seen)


def matches_played_generator(
    target_team_name: str,
    matches: Iterable[Match],
    skip_team_name: str | None = None,
) -> Iterable[Match]:
    """
    Get the matches played by a specific team with an optional team to skip

    :param target_team_name: The name of the team to get the matches for
    :param matches: The matches to filter
    :param skip_team_name: The name of the team to skip
    :return: The matches played by the target team
    :rtype: Iterable[Match]
    """
    for match in matches:
        if not (
            match.home_team == target_team_name or match.away_team == target_team_name
        ):
            continue

        if skip_team_name and (
            match.home_team == skip_team_name or match.away_team == skip_team_name
        ):
            continue

        yield match


def meetings_generator(
    team_name1: str | None, team_name2: str | None, matches: Iterable[Match]
) -> Iterable[Match]:
    """
    Get the matches between two teams
    """
    for match in matches:
        if not (match.home_team == team_name1 or match.away_team == team_name1):
            continue

        if not (match.home_team == team_name2 or match.away_team == team_name2):
            continue

        yield match


def opponent_names_generator(
    target_team_name: str | None, matches: Iterable[Match]
) -> Iterable[str]:
    """
    Get the names of the opponents of a specific team
    """
    if target_team_name is None:
        return

    for match in matches:
        if match.home_team == target_team_name:
            opponent_name = match.away_team
        elif match.away_team == target_team_name:
            opponent_name = match.home_team
        else:
            continue

        if opponent_name is None:
            continue

        yield opponent_name
