"""Advent of Code 2023 - Day 13

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
Grid = list[str]


def parse_data(filename: str) -> list[Grid]:
    with open(filename) as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    result = []
    current: list[str] = []
    for line in lines:
        if not line:
            result.append(current)
            current = []
        else:
            current.append(line)
    result.append(current)

    return result


def transpose(grid: Grid) -> Grid:
    # https://stackoverflow.com/a/23525479
    return list("".join(row) for row in zip(*grid))


def find_reflects_horizontal(grid: Grid) -> int:
    for y in range(1, len(grid)):
        if all(top == down for top, down in zip(reversed(grid[:y]), grid[y:])):
            return y
    return 0


def find_reflects_horizontal_smudge(grid: Grid) -> int:
    for y in range(1, len(grid)):
        smuges_required = 0
        for top, down in zip(reversed(grid[:y]), grid[y:]):
            smuges_required += sum(t != d for t, d in zip(top, down))

        if smuges_required == 1:
            return y

    return 0


def main() -> None:
    data = parse_data("input.txt")

    ##########
    # Part 1 #
    ##########

    result = 0
    for grid in data:
        horizontal = find_reflects_horizontal(grid)
        if horizontal:
            result += 100 * horizontal
        else:
            vertical = find_reflects_horizontal(transpose(grid))
            result += vertical

    assert result == 32371

    ##########
    # Part 2 #
    ##########

    result = 0
    for grid in data:
        horizontal = find_reflects_horizontal_smudge(grid)
        if horizontal:
            result += 100 * horizontal
        else:
            vertical = find_reflects_horizontal_smudge(transpose(grid))
            result += vertical

    assert result == 37416


if __name__ == "__main__":
    main()
