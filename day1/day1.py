import timing
import os
import sys

def part1():
    file = open(os.path.join(sys.path[0], "input_day1.txt"), "r")

    numbers = []

    for line in file:
        number = int(line)
        if 2020 - number in numbers:
            print(number*(2020-number))
            break
        if number not in numbers:
            numbers.append(number)

def part2():
    file = open(os.path.join(sys.path[0], "input_day1.txt"), "r")

    numbers = []
    sums={}
    for line in file:
        number = int(line)
        if 2020 - number in sums.keys():
            print(number*sums[2020-number]*((2020-number)-sums[2020-number]))
            break

        beginning_index = 0
        if number in numbers:
            beginning_index = (len(numbers) - numbers[::-1].index(number) - 1)

        for prev_number in numbers[beginning_index:]:
            sum = prev_number+number
            if sum not in sums.keys():
                sums[sum] = number

        numbers.append(number)

part1()

timing.log("part 1 done")

part2()

timing.log("part 2 done")