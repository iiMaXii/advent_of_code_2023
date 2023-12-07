"""Advent of Code 2023 - Day 7

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
from collections import Counter

RANKS = list(
    reversed(["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"])
)


@dataclass
class Hand:
    values: str

    def __init__(self, chars):
        self.values = []
        for c in chars:
            for n, r in enumerate(RANKS):
                if c == r:
                    self.values.append(n)
                    break

        assert len(chars) == len(self.values)

    def get_type(self):
        joker_value = RANKS.index("J")
        c = Counter(v for v in self.values if v != joker_value)
        c = sorted(c.items(), key=lambda item: item[1], reverse=True)

        joker_count = self.values.count(RANKS.index("J"))

        if joker_count == 5 or c[0][1] + joker_count == 5:
            # Five of a kind
            return 7

        if c[0][1] + joker_count == 4:
            # Four of a kind
            return 6

        if (
            (c[0][1] == 3 and c[1][1] == 2)
            or (joker_count == 1 and c[0][1] == 2 and c[1][1] == 2)
            or (joker_count == 1 and c[0][1] == 3)
        ):
            # Full house
            return 5

        if c[0][1] + joker_count == 3:
            # Three of a kind
            return 4

        if (
            (c[0][1] == 2 and c[1][1] == 2)
            or joker_count == 2
            or (joker_count == 1 and c[0][1] == 2)
        ):
            # Two pair
            return 3

        if c[0][1] + joker_count == 2:
            # One pair
            return 2

        return 1  # High card

    def __lt__(self, other: "Hand") -> bool:
        left_type = self.get_type()
        right_type = other.get_type()

        if left_type < right_type:
            return True

        if left_type == right_type:
            for lc, rc in zip(self.values, other.values):
                if lc < rc:
                    return True
                if lc > rc:
                    return False

        return False

    def __eq__(self, other: "Hand") -> bool:
        return self.values == other.values


def parse_data(filename: str):
    with open(filename) as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    res = []
    for line in lines:
        chars, num = line.split()
        assert len(chars) == 5
        res.append((Hand(chars), int(num)))

    return res


data = parse_data("input.txt")

data = sorted(data, key=lambda item: item[0])


result = 0
for rank, (hand, num) in enumerate(data, 1):
    print(rank, hand.get_type(), hand, num)
    result += rank * num

print(result)
assert result == 253362743
