from tools import timing
import os
import sys


def find_closest_timestamp_above_given_timestamp(schedule, timestamp):
    if timestamp % schedule == 0:
        return timestamp
    return schedule * (int(timestamp / schedule) + 1)


def day13():
    bus_schedules = []
    bus_ids = []
    bus_indexes = {}
    with open(os.path.join(sys.path[0], "day13/input_day13.txt"), "r") as file:
        lines = file.readlines()
        earliest_timestamp = int(lines[0].rstrip())
        closest_schedule = 0
        smallest_waiting_time = 0
        index = 0
        for bus_schedule in lines[1].rstrip().split(","):
            if bus_schedule != "x":
                bus_schedule = int(bus_schedule)
                bus_schedules.append((index, bus_schedule))
                bus_ids.append(bus_schedule)
                bus_indexes[bus_schedule] = bus_schedule - index

                closest_timestamp = find_closest_timestamp_above_given_timestamp(bus_schedule, earliest_timestamp)
                waiting_time = closest_timestamp - earliest_timestamp
                if closest_schedule == 0 or waiting_time < smallest_waiting_time:
                    smallest_waiting_time = waiting_time
                    closest_schedule = bus_schedule
            index += 1

    print("Solution part1: " + str(closest_schedule * smallest_waiting_time))

    timing.log("Part 1 is finished!")

    bus_ids.sort(reverse=True)

    current_value = bus_indexes[bus_ids[0]]
    increment = bus_ids[0]
    for index in range(1, len(bus_ids)):
        while current_value % bus_ids[index] != bus_indexes[bus_ids[index]] % bus_ids[index]:
            current_value += increment
        increment *= bus_ids[index]
    print("Solution part2: ", current_value)


