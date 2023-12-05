"""Advent of Code 2023 - Day 1

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

with open("input.txt") as f:
    lines = f.readlines()

##########
# Part 1 #
##########


def get_digit(line: str) -> int:
    for c in line:
        if c.isdigit():
            return int(c)

    raise ValueError(f"expected integer in line {line}")


digits = []
for line in lines:
    first_digit = get_digit(line)
    last_digit = get_digit(reversed(line))

    digits.append(first_digit * 10 + last_digit)

assert sum(digits) == 53334

##########
# Part 2 #
##########

DIGITS_ALPHA = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def get_digits(line):
    numbers = {}

    for n in range(1, 10):
        idx = line.find(str(n))
        if idx != -1:
            numbers[idx] = n

        idx = line.rfind(str(n))
        if idx != -1:
            numbers[idx] = n

    for n, a in enumerate(DIGITS_ALPHA):
        idx = line.find(a)
        if idx != -1:
            numbers[idx] = n + 1

        idx = line.rfind(a)
        if idx != -1:
            numbers[idx] = n + 1

    a = sorted(numbers.items())

    return a[0][1], a[-1][1]


numbers = []
for line in lines:
    first_digit, last_digit = get_digits(line)

    numbers.append(first_digit * 10 + last_digit)

assert sum(numbers) == 52834
