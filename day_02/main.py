"""Advent of Code 2023 - Day 2

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from dataclasses import dataclass


@dataclass
class Reveale:
    game_round: int
    r: int = 0
    g: int = 0
    b: int = 0


def parse_games(filename: str) -> list[list[Reveale]]:
    with open(filename) as f:
        lines = f.readlines()
    games: list[list[Reveale]] = []
    for n, line in enumerate(lines, 1):
        line = line.strip()

        assert line.startswith(f"Game {n}: ")
        _, line = line.split(":")

        game = []
        reveals = line.split("; ")

        for rev in reveals:
            color_reveal = Reveale(n)
            for r in rev.split(", "):
                if r.endswith(" red"):
                    color_reveal.r = int(r[:-4])
                elif r.endswith(" green"):
                    color_reveal.g = int(r[:-6])
                elif r.endswith(" blue"):
                    color_reveal.b = int(r[:-5])
                else:
                    raise RuntimeError(f'error show not be possible: "{r}"')

            game.append(color_reveal)
        games.append(game)
    return games


def include_game(game) -> bool:
    for r in game:
        if r.r > 12 or r.g > 13 or r.b > 14:
            return False
    return True


def get_fewest_power(game: list[Reveale]) -> int:
    """Part 2"""
    min_r = 0
    min_g = 0
    min_b = 0
    for r in game:
        min_r = max(min_r, r.r)
        min_g = max(min_g, r.g)
        min_b = max(min_b, r.b)
    return min_r * min_g * min_b


def main() -> None:
    games = parse_games("input.txt")

    ##########
    # Part 1 #
    ##########

    result = sum(n for n, game in enumerate(games, 1) if include_game(game))

    assert result == 2239

    ##########
    # Part 2 #
    ##########

    result = sum(get_fewest_power(g) for g in games)

    assert result == 83435


if __name__ == "__main__":
    main()
