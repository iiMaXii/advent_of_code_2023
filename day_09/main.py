"""Advent of Code 2023 - Day 9

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


def parse_data(filename: str) -> list[list[int]]:
    with open(filename) as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    numbers = []
    for line in lines:
        numbers.append(list(int(n) for n in line.split()))

    return numbers


def find_next_number(differences) -> int:
    all_differences = [differences]
    while any(n != 0 for n in differences):
        differences = [n - differences[i - 1] for i, n in enumerate(differences[1:], 1)]
        all_differences.append(differences)

    next_num = 0
    for seq in reversed(all_differences):
        next_num += seq[-1]
    return next_num


def find_previous_number(differences) -> int:
    all_differences = [differences]
    while any(n != 0 for n in differences):
        differences = [n - differences[i - 1] for i, n in enumerate(differences[1:], 1)]
        all_differences.append(differences)

    next_num = 0
    for seq in reversed(all_differences):
        next_num = seq[0] - next_num

    return next_num


def main() -> None:
    numbers = parse_data("input.txt")

    result = sum(find_next_number(seq) for seq in numbers)
    assert result == 2101499000

    result = sum(find_previous_number(seq) for seq in numbers)
    assert result == 1089


if __name__ == "__main__":
    main()
