"""Advent of Code 2023 - Day 5 (Part 2)

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
from typing import Optional, Tuple


def range_intersection(r1: range, r2: range) -> Optional[range]:
    start = max(r1.start, r2.start)
    stop = min(r1.stop, r2.stop)

    if start >= stop:
        return None

    return range(start, stop)


def range_left_disjoint(r1: range, r2: range) -> list[range]:
    intersection = range_intersection(r1, r2)
    if not intersection:
        return [r1]  # disjoint ranges

    result = []

    left_start = r1.start
    left_stop = r2.start
    if left_start < left_stop:
        result.append(range(left_start, left_stop))

    right_start = r2.stop
    right_stop = r1.stop
    if right_start < right_stop:
        result.append(range(right_start, right_stop))

    return result


# sanity check
assert range_intersection(range(10, 18), range(1, 14)) == range(10, 14)
assert range_left_disjoint(range(10, 18), range(1, 14)) == [range(14, 18)]
assert range_left_disjoint(range(1, 14), range(10, 18)) == [range(1, 10)]
assert range_left_disjoint(range(1, 20), range(10, 18)) == [range(1, 10), range(18, 20)]


def range_offset(r: range, offset: int) -> range:
    return range(r.start + offset, r.stop + offset)


@dataclass
class RangeFunction:
    in_range: range
    offset: int

    def __init__(self, source: int, dest: int, length: int):
        self.in_range = range(source, source + length)
        self.offset = dest - source

    def transform_range(self, input_range: range, rest: list) -> Optional[range]:
        intersection = range_intersection(self.in_range, input_range)

        for r in range_left_disjoint(input_range, self.in_range):
            rest.append(r)

        if not intersection:
            return None

        return range_offset(intersection, self.offset)


def parse_data(filename: str) -> Tuple[list[int], list[list[RangeFunction]]]:
    with open(filename) as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    assert lines[0].startswith("seeds: ")
    seeds = lines[0][len("seeds: ") :].split()
    seeds = list([int(s) for s in seeds])

    range_functions = []
    current_map = None
    for line in lines[1:]:
        if not line:
            continue

        if not line[0].isdigit():
            if current_map:
                range_functions.append(current_map)
            current_map = []
        else:
            dest, source, length = line.split()
            current_map.append(RangeFunction(int(source), int(dest), int(length)))

    range_functions.append(current_map)
    return seeds, range_functions


seeds, range_functions = parse_data("input.txt")

input_data = []
for n in range(0, len(seeds), 2):
    input_data.append(range(seeds[n], seeds[n] + seeds[n + 1]))

for stage in range_functions:
    results = []
    for func in stage:
        other = []
        for r in input_data:
            new_range = func.transform_range(r, other)
            if new_range:
                results.append(new_range)
        input_data = other

    input_data = results + input_data

assert min([r.start for r in input_data]) == 31161857
