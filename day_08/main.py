"""Advent of Code 2023 - Day 8

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
from itertools import cycle
from math import lcm


def parse_data(filename: str) -> tuple[str, dict[str, tuple[str, str]]]:
    with open(filename) as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    directions = lines[0]

    step_map = {}
    for line in lines[2:]:
        start, choises = line.split("=")
        l, r = choises.strip().strip("(").strip(")").split(",")

        step_map[start.strip()] = (l, r.strip())

    return directions, step_map


def main() -> None:
    directions, step_map = parse_data("input.txt")

    ##########
    # Part 1 #
    ##########

    steps_taken = 0
    next_step = "AAA"
    for direction in cycle(directions):
        steps_taken += 1
        next_map = step_map[next_step]
        if direction == "L":
            next_step = next_map[0]
        elif direction == "R":
            next_step = next_map[1]
        else:
            raise ValueError("unknown direction")

        if next_step == "ZZZ":
            break

    assert steps_taken == 22199

    ##########
    # Part 2 #
    ##########

    # Find start locations
    next_locations = []
    for start in step_map:
        if start.endswith("A"):
            next_locations.append(start)

    end_hit_after = [None for _ in next_locations]

    steps_taken = 0
    for direction in cycle(directions):
        steps_taken += 1

        for n, next_location in enumerate(next_locations):
            next_map = step_map[next_location]
            if direction == "L":
                next_step = next_map[0]
            elif direction == "R":
                next_step = next_map[1]
            else:
                raise ValueError("unknown direction")
            next_locations[n] = next_step

            if next_step.endswith("Z") and end_hit_after[n] is None:
                end_hit_after[n] = steps_taken

        if all(end for end in end_hit_after):
            break

    assert lcm(*end_hit_after) == 13334102464297


if __name__ == "__main__":
    main()
