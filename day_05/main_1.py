"""Advent of Code 2023 - Day 5 (Part 1)

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
from typing import Tuple


def parse_data(filename: str) -> Tuple[list[int], list[list[Tuple[int, int, int]]]]:
    with open(filename) as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    assert lines[0].startswith("seeds: ")
    seeds = lines[0][len("seeds: ") :].split()
    seeds = list([int(s) for s in seeds])

    seed_to_stuff = []
    current_map = None
    for line in lines[1:]:
        if not line:
            continue

        if not line[0].isdigit():
            if current_map:
                seed_to_stuff.append(current_map)
            current_map = []
        else:
            dest, source, length = line.split()
            current_map.append((int(dest), int(source), int(length)))

    seed_to_stuff.append(current_map)
    return seeds, seed_to_stuff


seeds, stuffs = parse_data("input.txt")


def get_seed_dest(seed, ranges):
    for r in ranges:
        if seed in range(r[1], r[1] + r[2]):
            return r[0] + (seed - r[1])
    return seed


wops = [s for s in seeds]
for stuff in stuffs:
    for n, w in enumerate(wops):
        wops[n] = get_seed_dest(w, stuff)

assert min(wops) == 57075758
