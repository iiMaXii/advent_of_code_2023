"""Advent of Code 2023 - Day 12

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
import functools


def parse_data(filename: str) -> list[tuple[str, tuple[int, ...]]]:
    with open(filename) as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    maps = []
    for line in lines:
        map, damaged_spring_counts_str = line.split()
        damaged_spring_counts = tuple(
            int(c) for c in damaged_spring_counts_str.split(",")
        )
        maps.append(
            (
                map,
                damaged_spring_counts,
            )
        )

    return maps


def fold_up(
    maps: list[tuple[str, tuple[int, ...]]]
) -> list[tuple[str, tuple[int, ...]]]:
    result = []
    for map, dmg in maps:
        new_map = "?".join(map for _ in range(5))
        result.append((new_map, dmg * 5))

    return result


assert fold_up([(".#", (1,))]) == [(".#?.#?.#?.#?.#", (1, 1, 1, 1, 1))]
assert fold_up([("???.###", (1, 1, 3))]) == [
    (
        "???.###????.###????.###????.###????.###",
        (1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3),
    )
]


@functools.cache
def get_permutations(map: str, dmg_counts: tuple[int, ...]) -> int:
    if not dmg_counts:
        if all(v in (".", "?") for v in map):
            return 1
        return 0

    right_dmg = dmg_counts[1:]

    left_dmg_count = dmg_counts[0]
    required_space_right = sum(right_dmg)
    if required_space_right > 0:
        required_space_right += len(right_dmg)

    required_space_right += left_dmg_count - 1

    count = 0
    for i in range(0, len(map) - required_space_right):
        if all(v in ("?", "#") for v in map[i : i + left_dmg_count]) and (
            i + left_dmg_count == len(map) or map[i + left_dmg_count] in (".", "?")
        ):
            new_map = map[i + left_dmg_count + 1 :].strip(".")
            new_dmg_count = dmg_counts[1:]
            count += get_permutations(new_map, new_dmg_count)

        if map[i] == "#":
            break

    return count


def main() -> None:
    maps = parse_data("input.txt")

    ##########
    # Part 1 #
    ##########

    counts = [get_permutations(map, dmg_counts) for map, dmg_counts in maps]
    assert sum(counts) == 7236

    ##########
    # Part 2 #
    ##########

    maps = fold_up(maps)

    counts = [get_permutations(map, dmg_counts) for map, dmg_counts in maps]
    assert sum(counts) == 11607695322318


if __name__ == "__main__":
    main()
