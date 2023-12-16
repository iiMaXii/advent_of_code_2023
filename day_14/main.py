"""Advent of Code 2023 - Day 14

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
Grid = list[list[str]]


def read_input(filename: str) -> Grid:
    with open(filename) as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    return list(list(c for c in line) for line in lines)


def rotate_cw(grid: Grid) -> Grid:
    return [list(row) for row in zip(*grid[::-1])]


def tilt_north(grid: Grid) -> None:
    for x, _ in enumerate(grid[0]):
        empty_place = None
        for y, _ in enumerate(grid):
            v = grid[y][x]
            if v == ".":
                if empty_place is None:
                    empty_place = y
            elif v == "#":
                empty_place = None
            elif v == "O":
                if empty_place is not None:
                    grid[empty_place][x] = "O"
                    grid[y][x] = "."
                    empty_place += 1
            else:
                raise ValueError()


def calc_load(grid: Grid) -> int:
    result = 0
    for y, row in enumerate(grid):
        for v in row:
            if v == "O":
                result += len(grid) - y
    return result


def main() -> None:
    grid = read_input("input.txt")

    ##########
    # Part 1 #
    ##########

    tilt_north(grid)
    result = calc_load(grid)
    assert result == 108955

    ##########
    # Part 2 #
    ##########

    # Just try to find a repeating sequence. Nothing fancy here

    rotations = 1000
    loads = []
    for _ in range(rotations):
        load = calc_load(grid)
        loads.append(load)
        for _ in range(4):
            tilt_north(grid)
            grid = rotate_cw(grid)

    # Find first repeating sequence
    cycle = None
    for count in range(5, 40):
        left = loads[-count * 2 : -count]
        right = loads[-count:]
        if left == right:
            cycle = count
            break

    assert cycle

    result = right[(1000000000 - rotations) % cycle]
    assert result == 106689


if __name__ == "__main__":
    main()
