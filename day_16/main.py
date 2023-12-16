"""Advent of Code 2023 - Day 16

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
from enum import Enum, auto
from typing import Generator


class Direction(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()


Grid = list[list[str]]
HistoryGrid = list[list[list[Direction]]]
Point = tuple[int, int]


def read_input(filename: str) -> Grid:
    with open(filename) as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    return list(list(c for c in line) for line in lines)


@dataclass
class Beam:
    coodinates: Point
    direction: Direction

    def move(self):
        x, y = self.coodinates
        if self.direction == Direction.WEST:
            self.coodinates = (x - 1, y)
        elif self.direction == Direction.EAST:
            self.coodinates = (x + 1, y)
        elif self.direction == Direction.NORTH:
            self.coodinates = (x, y - 1)
        elif self.direction == Direction.SOUTH:
            self.coodinates = (x, y + 1)


def remove_out_of_bounds(beams: list[Beam], x_bound: int, y_bound: int) -> None:
    out_of_bounds = list(
        beam
        for beam in beams
        if 0 > beam.coodinates[0]
        or beam.coodinates[0] >= x_bound
        or 0 > beam.coodinates[1]
        or beam.coodinates[1] >= y_bound
    )
    for o in out_of_bounds:
        beams.remove(o)


MIRROR_DIRECTIONS = {
    "/": {
        Direction.WEST: Direction.SOUTH,
        Direction.NORTH: Direction.EAST,
        Direction.EAST: Direction.NORTH,
        Direction.SOUTH: Direction.WEST,
    },
    "\\": {
        Direction.WEST: Direction.NORTH,
        Direction.NORTH: Direction.WEST,
        Direction.EAST: Direction.SOUTH,
        Direction.SOUTH: Direction.EAST,
    },
}


def do_tick(grid: Grid, beams: list[Beam], history: HistoryGrid):
    new_beams: list[Beam] = []

    for beam in beams:
        beam.move()

    remove_out_of_bounds(beams, len(grid[0]), len(grid))

    # Calc new beams and new directions
    for beam in beams:
        x, y = beam.coodinates
        d = beam.direction
        if grid[y][x] in MIRROR_DIRECTIONS:
            d = MIRROR_DIRECTIONS[grid[y][x]][d]
        elif grid[y][x] == "-":
            if d in (Direction.NORTH, Direction.SOUTH):
                d = Direction.WEST
                new_beams.append(Beam((x, y), Direction.EAST))
        elif grid[y][x] == "|":
            if d in (Direction.WEST, Direction.EAST):
                d = Direction.NORTH
                new_beams.append(Beam((x, y), Direction.SOUTH))
        beam.direction = d

    beams.extend(new_beams)

    # Mark visited and remove duplicates
    duplicate_beams = []
    for beam in beams:
        x, y = beam.coodinates
        if beam.direction not in history[y][x]:
            history[y][x].append(beam.direction)
        else:
            duplicate_beams.append(beam)
    for dup in duplicate_beams:
        beams.remove(dup)


def get_all_start_points(grid: Grid) -> Generator[Beam, None, None]:
    for y in range(len(grid)):
        yield Beam((-1, y), Direction.EAST)

    for y in range(len(grid)):
        yield Beam((len(grid), y), Direction.WEST)

    for x in range(len(grid[0])):
        yield Beam((x, -1), Direction.SOUTH)

    for x in range(len(grid[0])):
        yield Beam((x, len(grid[0])), Direction.NORTH)


def calc_score(grid: HistoryGrid) -> int:
    score = 0
    for row in grid:
        for v in row:
            if v:
                score += 1
    return score


def main() -> None:
    data = read_input("input.txt")

    ##########
    # Part 1 #
    ##########

    history: HistoryGrid = [[[] for _ in row] for row in data]
    beams: list[Beam] = [Beam((-1, 0), Direction.EAST)]
    do_tick(data, beams, history)

    while beams:
        do_tick(data, beams, history)

    result = calc_score(history)
    assert result == 8021

    ##########
    # Part 2 #
    ##########

    result = 0
    for b in get_all_start_points(data):
        beams = [b]
        history = [[[] for _ in row] for row in data]
        while beams:
            do_tick(data, beams, history)
        result = max(result, calc_score(history))

    assert result == 8216


if __name__ == "__main__":
    main()
