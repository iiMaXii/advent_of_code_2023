"""Advent of Code 2023 - Day 15

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


def read_input(filename: str) -> list[str]:
    with open(filename) as f:
        lines = f.readlines()

    return list(lines[0].split(","))


def calc_hash(data: str) -> int:
    h = 0
    for c in data:
        h += ord(c)
        h *= 17
        h %= 256
    return h


def split_instruction(data: str) -> tuple[str, str, str]:
    key, value = data.replace("-", "=").split("=")
    seperator = data[len(key)]
    return key, seperator, value


@dataclass
class Lens:
    label: str
    focal_length: int

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Lens):
            return self.label == other.label

        if isinstance(other, str):
            return self.label == other

        raise ValueError()


def main() -> None:
    data = read_input("input.txt")

    ##########
    # Part 1 #
    ##########

    result = sum(calc_hash(d) for d in data)
    assert result == 513158

    ##########
    # Part 2 #
    ##########

    boxes: list[list[Lens]] = [[] for _ in range(256)]
    for d in data:
        key, seperator, value = split_instruction(d)

        box = boxes[calc_hash(key)]
        if seperator == "-":
            try:
                box.remove(key)
            except ValueError:
                pass
        elif seperator == "=":
            lens = Lens(key, int(value))
            try:
                i = box.index(lens)
                box[i] = lens
            except ValueError:
                box.append(lens)
        else:
            raise ValueError()

    result = 0
    for box_number, box in enumerate(boxes, 1):
        for slot_number, v in enumerate(box, 1):
            result += box_number * slot_number * v.focal_length

    assert result == 200277


if __name__ == "__main__":
    main()
