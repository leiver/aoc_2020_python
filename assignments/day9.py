from tools import timing
import os
import sys


def day9():
    numbers_parsed = []

    with open(os.path.join(sys.path[0], "inputs/input_day9.txt"), "r") as file:
        for line in file:
            number_to_parse = int(line.rstrip())

            if len(numbers_parsed) >= 25:
                found_match = False
                for first_number in range(1, 25):
                    for second_number in range(first_number + 1, 26):
                        if numbers_parsed[len(numbers_parsed) - first_number] + numbers_parsed[len(numbers_parsed) - second_number] == number_to_parse:
                            found_match = True
                            break
                    if found_match:
                        break
                if not found_match:
                    invalid_number = number_to_parse
                    break

            numbers_parsed.append(number_to_parse)

    print("Solution part1: " + str(invalid_number))

    timing.log("Part 1 finished!")

    start_range_index = 0
    current_sum = numbers_parsed[0]
    for end_range_index in range(1, len(numbers_parsed)):
        new_number = numbers_parsed[end_range_index]
        new_sum = current_sum + new_number
        while new_sum > invalid_number:
            old_number = numbers_parsed[start_range_index]
            new_sum -= old_number
            start_range_index += 1
        if new_sum == invalid_number:
            list_of_numbers = numbers_parsed[start_range_index:end_range_index+1]
            smallest_number = min(list_of_numbers)
            largest_number = max(list_of_numbers)
            result = smallest_number + largest_number
            break
        current_sum = new_sum

    print("Solution part2: " + str(result))
