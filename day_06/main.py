"""Advent of Code 2023 - Day 6

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


def parse_data(filename: str):
    with open(filename) as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    assert lines[0].startswith('Time:      ')
    times = [int(t) for t in lines[0][len('Time:      '):].split() if t]
    assert lines[1].startswith('Distance:  ')
    distance = [int(t) for t in lines[1][len('Distance:  '):].split() if t]

    return times, distance



def ways_to_win(current_winning_time: int, winning_distance: int):
    count = 0
    for hold_time in range(1, current_winning_time):
        distance = hold_time * (current_winning_time - hold_time)
        if distance > winning_distance:
            count += 1
    return count

times, distance = parse_data("input.txt")

##########
# Part 1 #
##########

s = 1
for t, d in zip(times, distance):
    s*=ways_to_win(t, d)
print(s)

##########
# Part 2 #
##########

# the parsing was unnecessary since it took longer to write that then just putting the numbers here directly :)

time = 44806572
distance = 208158110501102
print(ways_to_win(time, distance))
