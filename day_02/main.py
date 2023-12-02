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

# Quick and dirty solution
# Sorry for bad code :)


from dataclasses import dataclass

with open('input.txt') as f:
    lines = f.readlines()

@dataclass
class Reveale:
    game_round: int
    r: int = 0
    g: int = 0
    b: int = 0

##########
# Task 1 #
##########

games: list[list[Reveale]] = []
for n, line in enumerate(lines, 1):
    line = line.strip()

    assert line.startswith(f'Game {n}: ')
    _, line = line.split(':')

    game = []
    reveals = line.split('; ')

    for rev in reveals:
        color_reveal = Reveale(n)
        for r in rev.split(', '):
            if r.endswith(' red'):
                color_reveal.r = int(r[:-4])
            elif r.endswith(' green'):
                color_reveal.g = int(r[:-6])
            elif r.endswith(' blue'):
                color_reveal.b = int(r[:-5])
            else:
                raise RuntimeError(f'error show not be possible: "{r}"')
        
        game.append(color_reveal)
    games.append(game)


count = 0
for g in games:
    possible = True
    for r in g:
        if r.r > 12 or r.g > 13 or r.b > 14:
            possible = False
    if possible:
        count += r.game_round

assert count == 2239

##########
# Task 2 #
##########

def get_fewest_power(game):
    min_r = 0
    min_g = 0
    min_b = 0
    for r in game:
        min_r = max(min_r, r.r)
        min_g = max(min_g, r.g)
        min_b = max(min_b, r.b)
    return min_r * min_g * min_b

sum = 0
for g in games:
    p = get_fewest_power(g)
    sum += p

assert sum == 83435
