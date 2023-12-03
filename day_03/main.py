"""Advent of Code 2023 - Day 3

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
from dataclasses import dataclass, field
from typing import Optional


with open('input.txt') as f:
    lines = f.readlines()

lines = [line.strip() for line in lines]

@dataclass(frozen=True)
class Point:
    x: int
    y: int

@dataclass
class SchemaNumber:
    number: int
    coordinates: list[Point] = field(default_factory=list)

@dataclass
class SchemaSymbol:
    value: str
    coordinates: Point

# Parse schema
symbols: list[SchemaSymbol] = []
part_numbers: list[SchemaNumber] = []
for y, row in enumerate(lines):
    current_part_number: Optional[SchemaNumber] = None
    for x, c in enumerate(row):
        if c.isdigit():
            if current_part_number:
                current_part_number.number = current_part_number.number*10 + int(c)
            else:
                current_part_number = SchemaNumber(int(c))

            current_part_number.coordinates.append(Point(x, y))
        else:
            if current_part_number:
                part_numbers.append(current_part_number)
                current_part_number = None
            if c == '.':
                continue # not a symbol apparently

            # symbol
            symbols.append(SchemaSymbol(value=c, coordinates=Point(x, y)))

    # this part is important not to miss
    if current_part_number:
        part_numbers.append(current_part_number)
        current_part_number = None

##########
# Part 1 #
##########

def has_common_point(points_lhs, points_rhs)-> bool:
    for l in points_lhs:
        if l in points_rhs:
            return True
    return False

def get_adjacent_numbers(part_numbers: list[SchemaNumber], p: Point) -> list[SchemaNumber]:
    adjacent_points = [
        Point(p.x - 1, p.y - 1),
        Point(p.x,     p.y - 1),
        Point(p.x + 1, p.y - 1),

        Point(p.x - 1, p.y),
        # Point(p.x, p.y),
        Point(p.x + 1, p.y),

        Point(p.x - 1, p.y + 1),
        Point(p.x,     p.y + 1),
        Point(p.x + 1, p.y + 1),
    ]

    numbers = []
    for part in part_numbers:
        if has_common_point(part.coordinates, adjacent_points):
            numbers.append(part)
    
    return numbers

result = []
for sym in symbols:
    for adj in get_adjacent_numbers(part_numbers, sym.coordinates):
        if adj not in result:
            result.append(adj)

assert sum([r.number for r in result]) == 556367

##########
# Part 2 #
##########

res = 0
for sym in symbols:
    if sym.value == '*':
        adj = get_adjacent_numbers(part_numbers, sym.coordinates)
        if len(adj) == 2:
            res += adj[0].number * adj[1].number 

assert res == 89471771
