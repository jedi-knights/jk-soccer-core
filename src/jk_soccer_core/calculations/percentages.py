from collections.abc import Iterable

from jk_soccer_core import Match


def build_team_index(matches: list[Match]) -> dict[str, list[Match]]:
    """Index matches by participating team for O(1) lookup of a team's matches."""
    index: dict[str, list[Match]] = {}
    for m in matches:
        if m.home_team is not None:
            index.setdefault(m.home_team, []).append(m)
        if m.away_team is not None:
            index.setdefault(m.away_team, []).append(m)
    return index


def _wld_tally(
    team: str, team_matches: list[Match], skip: str | None
) -> tuple[int, int, int]:
    """Single-pass tally of (wins, losses, draws) for ``team`` over its matches.

    ``team_matches`` is presumed to already involve ``team`` (e.g. from a team
    index). Penalty-shootout matches always count as draws regardless of score.
    Matches involving ``skip`` are excluded.
    """
    wins = losses = draws = 0
    for m in team_matches:
        if skip is not None and (m.home_team == skip or m.away_team == skip):
            continue
        if m.penalty_shootout or m.home_score == m.away_score:
            draws += 1
            continue
        is_home = m.home_team == team
        team_won = (is_home and m.home_score > m.away_score) or (
            not is_home and m.away_score > m.home_score
        )
        if team_won:
            wins += 1
        else:
            losses += 1
    return wins, losses, draws


class WinningPercentageCalculation:
    """Calculate the winning percentage for a specific team.

    The tie value is configurable to support multiple RPI methodologies:
    - 0.5 (default): traditional NCAA RPI; ECNL; pre-2024 NCAA women's soccer
    - 1/3: NCAA 2024+ women's soccer Element 1 (per CP Thomas spec)
    """

    def __init__(
        self,
        team_name: str | None,
        skip_team_name: str | None = None,
        number_of_digits: int = 2,
        tie_value: float = 0.5,
    ):
        self.__team_name = team_name
        self.__skip_team_name = skip_team_name
        self.__number_of_digits = number_of_digits
        self.__tie_value = tie_value

    def _compute_indexed(self, index: dict[str, list[Match]]) -> float:
        """Return the WP at full precision using a prebuilt team index."""
        if not self.__team_name:
            return 0.0
        team_matches = index.get(self.__team_name)
        if not team_matches:
            return 0.0
        wins, losses, draws = _wld_tally(
            self.__team_name, team_matches, self.__skip_team_name
        )
        played = wins + losses + draws
        if played == 0:
            return 0.0
        return (float(wins) + float(draws) * self.__tie_value) / float(played)

    def _compute(self, matches: Iterable[Match]) -> float:
        """Return the winning percentage at full precision (no rounding)."""
        return self._compute_indexed(build_team_index(list(matches)))

    def calculate(self, matches: Iterable[Match]) -> float:
        """Calculate the winning percentage for a specific team."""
        return round(self._compute(matches), self.__number_of_digits)


class OpponentsWinningPercentageCalculation:
    """Calculate the average winning percentage of a team's opponents.

    For each opponent encounter (weighted by meeting count), the opponent's WP
    is computed with games against the target team excluded — implementing the
    standard NCAA RPI Element 2 opponent-removal logic.
    """

    def __init__(
        self,
        team_name: str | None,
        number_of_digits: int = 2,
        tie_value: float = 0.5,
    ):
        self.__team_name = team_name
        self.__number_of_digits = number_of_digits
        self.__tie_value = tie_value

    def _compute_indexed(self, index: dict[str, list[Match]]) -> float:
        """Return the OWP at full precision using a prebuilt team index.

        Opponents are grouped by unique name so each opponent's WP is
        computed once and multiplied by the encounter count, rather than
        recomputed on every encounter (per-encounter weighting per the
        NCAA RPI Element 2 spec is preserved).
        """
        team = self.__team_name
        if not team:
            return 0.0
        team_matches = index.get(team)
        if not team_matches:
            return 0.0

        encounters: dict[str, int] = {}
        for m in team_matches:
            opponent = m.away_team if m.home_team == team else m.home_team
            if opponent is None:
                continue
            encounters[opponent] = encounters.get(opponent, 0) + 1

        if not encounters:
            return 0.0

        total = 0
        weighted_sum = 0.0
        for opponent, count in encounters.items():
            wp = WinningPercentageCalculation(
                opponent,
                team,
                self.__number_of_digits,
                tie_value=self.__tie_value,
            )._compute_indexed(index)
            weighted_sum += wp * count
            total += count

        return weighted_sum / float(total)

    def _compute(self, matches: Iterable[Match]) -> float:
        """Return the OWP at full precision (no rounding)."""
        return self._compute_indexed(build_team_index(list(matches)))

    def calculate(self, matches: Iterable[Match]) -> float:
        """Calculate the winning percentage of the opponents of a specific team."""
        return round(self._compute(matches), self.__number_of_digits)


class OpponentsOpponentsWinningPercentageCalculation:
    """Calculate the average OWP of a team's opponents (RPI Element 3).

    For each of the team's opponents X, this computes X's own opponents'
    winning percentage — where each opponent-of-X's record excludes games
    against X (not against the original team).
    """

    def __init__(
        self,
        team_name: str | None,
        number_of_digits: int = 2,
        tie_value: float = 0.5,
    ):
        self.__team_name = team_name
        self.__number_of_digits = number_of_digits
        self.__tie_value = tie_value

    def _compute_indexed(self, index: dict[str, list[Match]]) -> float:
        """Return the OOWP at full precision using a prebuilt team index.

        Opponents are grouped by unique name so each opponent's OWP is
        computed once and multiplied by the encounter count.
        """
        team = self.__team_name
        if not team:
            return 0.0
        team_matches = index.get(team)
        if not team_matches:
            return 0.0

        encounters: dict[str, int] = {}
        for m in team_matches:
            opponent = m.away_team if m.home_team == team else m.home_team
            if opponent is None:
                continue
            encounters[opponent] = encounters.get(opponent, 0) + 1

        if not encounters:
            return 0.0

        total = 0
        weighted_sum = 0.0
        for opponent, count in encounters.items():
            owp = OpponentsWinningPercentageCalculation(
                opponent,
                self.__number_of_digits,
                tie_value=self.__tie_value,
            )._compute_indexed(index)
            weighted_sum += owp * count
            total += count

        return weighted_sum / float(total)

    def _compute(self, matches: Iterable[Match]) -> float:
        """Return the OOWP at full precision (no rounding)."""
        return self._compute_indexed(build_team_index(list(matches)))

    def calculate(self, matches: Iterable[Match]) -> float:
        """Calculate the OOWP of a specific team."""
        return round(self._compute(matches), self.__number_of_digits)
