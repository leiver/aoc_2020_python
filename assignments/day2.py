from tools import timing
import os
import sys


def day2():
    part1()

    timing.log("Part 1 finished!")

    part2()


def part1():
    file = open(os.path.join(sys.path[0], "inputs/input_day2.txt"), "r")

    valid_passwords = 0

    for line in file:
        split_line = line.split()

        bounds = split_line[0].split("-")
        character = split_line[1][0]
        password = split_line[2]

        occurrences = password.count(character)
        if int(bounds[0]) <= occurrences <= int(bounds[1]):
            valid_passwords += 1

    print(valid_passwords)


def part2():
    file = open(os.path.join(sys.path[0], "inputs/input_day2.txt"), "r")

    valid_passwords = 0

    for line in file:
        split_line = line.split()

        bounds = split_line[0].split("-")
        character = split_line[1][0]
        password = split_line[2]

        first_position = password[int(bounds[0]) - 1]
        second_position = password[int(bounds[1]) - 1]

        if (first_position == character and second_position != character) or (
                first_position != character and second_position == character):
            valid_passwords += 1

    print(valid_passwords)
