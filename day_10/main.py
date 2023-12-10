"""Advent of Code 2023 - Day 10

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
from enum import Enum, auto
from typing import Iterable

Point = tuple[int, int]
Grid = list[list[str | None]]  # note only one char for each element


def parse_data(filename: str) -> Grid:
    with open(filename) as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    grid: Grid = list(list(c for c in line) for line in lines)

    return grid


def get_start_point(data: Grid) -> Point:
    for y, row in enumerate(data):
        for x, v in enumerate(row):
            if v == "S":
                return (x, y)

    raise ValueError("unable to find start")


def get_next_points(point: Point, data: Grid) -> list[Point]:
    """Get the next possible coorinates to walk to.
    The result should contain two points if the input data is sane."""
    x, y = point
    connecting_points = []
    if data[y][x] == "-":
        if data[y][x - 1] in ("-", "F", "L", "S"):
            connecting_points.append((x - 1, y))
        if data[y][x + 1] in ("-", "7", "J", "S"):
            connecting_points.append((x + 1, y))
    elif data[y][x] == "|":
        if data[y - 1][x] in ("|", "F", "7", "S"):
            connecting_points.append((x, y - 1))
        if data[y + 1][x] in ("|", "L", "J", "S"):
            connecting_points.append((x, y + 1))
    elif data[y][x] == "F":
        if data[y][x + 1] in ("-", "7", "J", "S"):
            connecting_points.append((x + 1, y))
        if data[y + 1][x] in ("|", "L", "J", "S"):
            connecting_points.append((x, y + 1))
    elif data[y][x] == "7":
        if data[y][x - 1] in ("-", "F", "L", "S"):
            connecting_points.append((x - 1, y))
        if data[y + 1][x] in ("|", "L", "J", "S"):
            connecting_points.append((x, y + 1))
    elif data[y][x] == "J":
        if data[y - 1][x] in ("|", "F", "7", "S"):
            connecting_points.append((x, y - 1))
        if data[y][x - 1] in ("-", "L", "F", "S"):
            connecting_points.append((x - 1, y))
    elif data[y][x] == "L":
        if data[y - 1][x] in ("|", "F", "7", "S"):
            connecting_points.append((x, y - 1))
        if data[y][x + 1] in ("-", "7", "J", "S"):
            connecting_points.append((x + 1, y))
    else:
        raise RuntimeError(f"not a recognized shape {data[y][x]}")

    return connecting_points


def get_from_start(point: Point, data: Grid) -> list[Point]:
    """Special case for start since we do not know the directions from the value."""
    x, y = point
    connecting_points = []
    assert data[y][x] == "S"
    if data[y][x - 1] in ("-", "F", "L"):
        connecting_points.append((x - 1, y))
    if data[y][x + 1] in ("-", "7", "J"):
        connecting_points.append((x + 1, y))
    if data[y - 1][x] in ("|", "F", "7"):
        connecting_points.append((x, y - 1))
    if data[y + 1][x] in ("|", "L", "J"):
        connecting_points.append((x, y + 1))
    return connecting_points


def is_start(point: Point, data: Grid) -> bool:
    x, y = point
    return data[y][x] == "S"


# Part 2 functions, now it gets a bit ugly. There is probably an easier way to solve this.


def create_clean_copy(data: Grid, tunnel_coordinates: Iterable[Point]) -> Grid:
    """Create a copy with only the tunnel, everything else is set to None
    Also make it bigger so we dont have to handle edges and corners"""
    clean_copy: Grid = [
        [None for _ in range(len(data[0]) + 2)] for _ in range(len(data) + 2)
    ]
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            if (x, y) in tunnel_coordinates:
                clean_copy[y + 1][x + 1] = value
    return clean_copy


def find_connected_points_and_mark(data: Grid, point: Point) -> list[Point]:
    """Mark the supplied point as inside and also mark any adjacent points."""
    x, y = point
    search_points = [
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x - 1, y),
        (x, y),
        (x + 1, y),
        (x - 1, y + 1),
        (x, y + 1),
        (x + 1, y + 1),
    ]

    # discard invalid points
    search_points = [
        (x, y)
        for x, y in search_points
        if x in range(0, len(data[0])) and y in range(0, len(data))
    ]
    # discard taken points
    search_points = [(x, y) for x, y in search_points if data[y][x] is None]
    # mark as taken
    for x, y in search_points:
        data[y][x] = "I"

    return search_points


def fill_inside(point: Point, data: Grid) -> None:
    """Mark all the adjacent coordinates as inside "recursively"."""
    stack = [point]
    while stack:
        p = stack.pop()
        new_points = find_connected_points_and_mark(data, p)
        stack.extend(new_points)


class Direction(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()

    @staticmethod
    def from_coords(c1: Point, c2: Point) -> "Direction":
        x1, y1 = c1
        x2, y2 = c2

        if x1 > x2 and y1 == y2:
            return Direction.WEST
        if x1 < x2 and y1 == y2:
            return Direction.EAST
        if x1 == x2 and y1 > y2:
            return Direction.NORTH
        if x1 == x2 and y1 < y2:
            return Direction.SOUTH

        raise ValueError("cant determine direction of points")


# Assume the inside is on the right (this might not be the case for all inputs)
def get_possible_inside_right(
    point: Point, direction: Direction, data: Grid
) -> list[Point]:
    x, y = point
    value = data[y][x]
    if value == "-":
        if direction == Direction.EAST:
            return [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
        if direction == Direction.WEST:
            return [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]
        raise ValueError()
    if value == "|":
        if direction == Direction.NORTH:
            return [(x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]
        if direction == Direction.SOUTH:
            return [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1)]
        raise ValueError()
    if value == "7":
        if direction == Direction.EAST:
            return [(x - 1, y + 1)]
        if direction == Direction.NORTH:
            return [(x, y - 1), (x + 1, y - 1), (x + 1, y)]
        raise ValueError()
    if value == "J":
        if direction == Direction.EAST:
            return [(x + 1, y), (x + 1, y + 1), (x, y + 1)]
        if direction == Direction.SOUTH:
            return [(x - 1, y - 1)]
        raise ValueError()
    if value == "L":
        if direction == Direction.WEST:
            return [(x + 1, y - 1)]
        if direction == Direction.SOUTH:
            return [(x - 1, y), (x - 1, y + 1), (x, y + 1)]
        raise ValueError()
    if value == "F":
        if direction == Direction.NORTH:
            return [(x + 1, y + 1)]
        if direction == Direction.WEST:
            return [(x, y - 1), (x - 1, y - 1), (x - 1, y)]
        raise ValueError()
    raise ValueError(f"unknown tile {value}")


def main() -> None:
    ##########
    # Part 1 #
    ##########
    data = parse_data("input.txt")

    previous_position = get_start_point(data)
    next_positions = get_from_start(previous_position, data)

    assert len(next_positions) == 2
    current_position = next_positions[
        0
    ]  # just pick one direction, we will hopefully loop around

    all_tunnel_coordinates = {previous_position, current_position}
    while not is_start(current_position, data):
        next_positions = get_next_points(current_position, data)
        next_positions.remove(previous_position)  # we dont want to go back
        assert len(next_positions) == 1

        previous_position = current_position
        current_position = next_positions[0]
        all_tunnel_coordinates.add(current_position)

    assert len(all_tunnel_coordinates) % 2 == 0
    result = len(all_tunnel_coordinates) // 2
    print(result)
    assert result == 6890

    ##########
    # Part 2 #
    ##########

    clean_copy = create_clean_copy(data, all_tunnel_coordinates)

    previous_position = get_start_point(clean_copy)

    next_positions = get_from_start(previous_position, clean_copy)
    assert len(next_positions) == 2
    current_position = next_positions[0]

    while not is_start(current_position, clean_copy):
        direction = Direction.from_coords(previous_position, current_position)

        possible_inside = get_possible_inside_right(
            current_position, direction, clean_copy
        )

        for x, y in possible_inside:
            if clean_copy[y][x] is None:
                fill_inside((x, y), clean_copy)

        next_positions = get_next_points(current_position, clean_copy)
        next_positions.remove(previous_position)

        assert len(next_positions) == 1

        previous_position = current_position
        current_position = next_positions[0]

    inside_area = 0
    for row in clean_copy:
        for v in row:
            if v == "I":
                inside_area += 1

    print(inside_area)
    assert inside_area == 453


if __name__ == "__main__":
    main()
