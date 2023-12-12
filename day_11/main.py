"""Advent of Code 2023 - Day 11

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
Point = tuple[int, int]
Grid = list[list[str]]  # note only one char for each element


def parse_data(filename: str) -> Grid:
    with open(filename) as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    grid: Grid = list(list(c for c in line) for line in lines)

    return grid


def get_expansion_slices(data: Grid) -> tuple[list[int], list[int]]:
    rows_to_expand = []
    cols_to_expand = []
    for y, row in enumerate(data):
        if all(v == "." for v in row):
            rows_to_expand.append(y)

    for x, _ in enumerate(data[0]):
        if all(row[x] == "." for row in data):
            cols_to_expand.append(x)
    return cols_to_expand, rows_to_expand


def get_points(data: Grid) -> list[Point]:
    points = []
    for y, row in enumerate(data):
        for x, v in enumerate(row):
            if v == "#":
                points.append((x, y))
    return points


def get_distance_sum(
    points: list[Point], cols: list[int], rows: list[int], multiplier: int
) -> int:
    distance = 0
    for n, p1 in enumerate(points):
        for p2 in points[n + 1 :]:
            x1, y1 = p1
            x2, y2 = p2
            x1_offset = 0
            x2_offset = 0
            for x in cols:
                if x1 < x < x2:
                    x2_offset += multiplier - 1
                elif x2 < x < x1:
                    x1_offset += multiplier - 1
            y1_offset = 0
            y2_offset = 0
            for y in rows:
                if y1 < y < y2:
                    y2_offset += multiplier - 1
                elif y2 < y < y1:
                    y1_offset += multiplier - 1

            x1 += x1_offset
            x2 += x2_offset
            y1 += y1_offset
            y2 += y2_offset

            distance += abs(x1 - x2) + abs(y1 - y2)

    return distance


def main() -> None:
    data = parse_data("input.txt")

    points = get_points(data)
    cols, rows = get_expansion_slices(data)

    distance = get_distance_sum(points, cols, rows, 2)
    assert distance == 9681886

    distance = get_distance_sum(points, cols, rows, 1000000)
    assert distance == 791134099634


if __name__ == "__main__":
    main()
