from tools import timing
import os
import sys


def day15():
    numbers = {6: 0, 13: 1, 1: 2, 15: 3, 2: 4, 0: 5}
    last_number = 0
    for index in range(len(numbers), 2019):
        if last_number in numbers:
            last_number_index = numbers.get(last_number)
            numbers[last_number] = index
            last_number = index - last_number_index
        else:
            numbers[last_number] = index
            last_number = 0

    print("Solution part1: ", last_number)

    timing.log("Part 1 finished!")

    numbers = {6: 0, 13: 1, 1: 2, 15: 3, 2: 4, 0: 5}
    last_number = 0
    for index in range(len(numbers), 29999999):
        if last_number in numbers:
            last_number_index = numbers.get(last_number)
            numbers[last_number] = index
            last_number = index - last_number_index
        else:
            numbers[last_number] = index
            last_number = 0

    print("Solution part2: ", last_number)
