from tools import timing
import os
import sys


def add_adapter_to_jolt_map(adapter_to_add, jolt_map):
    for i in range(1, 4):
        if adapter_to_add - i < 0:
            break
        adapters_count = 0
        if adapter_to_add - i in jolt_map:
            adapters_count = jolt_map[adapter_to_add - i]
        adapters_count += 1
        jolt_map[adapter_to_add - i] = adapters_count


def day10():
    highest_adapter = 0
    adapters = [0]
    adapters_for_jolt = {}
    with open(os.path.join(sys.path[0], "inputs/input_day10.txt"), "r") as file:
        for line in file:
            adapter = int(line.rstrip())
            adapters.append(adapter)
            highest_adapter = max([adapter, highest_adapter])

            add_adapter_to_jolt_map(adapter, adapters_for_jolt)

    adapters.append(highest_adapter + 3)
    add_adapter_to_jolt_map(highest_adapter + 3, adapters_for_jolt)

    adapters = sorted(adapters)

    difference_of_1 = 0
    difference_of_3 = 0

    possible_arrangements = 1
    previous_adapter_count = 1
    current_jolt = 0
    consecutive_3s = 0
    for adapter in adapters:
        if adapter in adapters_for_jolt:
            adapter_count = adapters_for_jolt[adapter]
            if adapter_count > 1 and adapter_count >= previous_adapter_count:
                if adapter_count == 2:
                    possible_arrangements *= 2
                elif adapter_count == 3:
                    consecutive_3s += 1
            elif consecutive_3s > 0:
                possible_arrangements *= (3 * pow(2, consecutive_3s-1)) + 1
                consecutive_3s = 0
            previous_adapter_count = adapter_count

        jolt_difference = adapter - current_jolt
        current_jolt = adapter
        if jolt_difference == 1:
            difference_of_1 += 1
        elif jolt_difference == 3:
            difference_of_3 += 1

    print("Solution part1: " + str(difference_of_1 * difference_of_3))

    print("Solution part2: " + str(possible_arrangements))
