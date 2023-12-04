"""Advent of Code 2023 - Day 4

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

def parse_numbers(filename: str) -> list[list]:
    with open('input.txt') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    cards = []
    for n, line in enumerate(lines, 1):
        assert line.startswith(f'Card {n:>3}: ')
        line = line[len(f'Card {n:>3}: '):]

        win, your = line.split('|')
        win = win.strip().split(' ')
        your = your.strip().split(' ')

        # Remove blank spaces from splitting
        win = [w for w in win if w]
        your = [w for w in your if w]

        winning = [int(w) for w in win]
        my_numbers = [int(y) for y in your]

        cards.append([winning, my_numbers])

    return cards

cards = parse_numbers('input.txt')

##########
# Part 1 #
##########

total = 0
for card in cards:
    round_points = 0
    for win in card[0]:
        if win in card[1]:
            if round_points == 0:
                round_points = 1
            else:
                round_points *= 2
    total += round_points

assert total == 19135

##########
# Part 2 #
##########

card_count = [1 for _ in cards]
for game_num, card in enumerate(cards):
    round_multiplier = card_count[game_num]
    round_wins = 0
    for win in card[0]:
        if win in card[1]:
            round_wins += 1
    
    # increase card counts
    for i in range(game_num+1, game_num+round_wins+1):
        if i > len(card_count):
            break
        card_count[i] += 1 * round_multiplier

assert sum(card_count) == 5704953
