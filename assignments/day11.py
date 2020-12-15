from tools import timing
import os
import sys
import copy

directions_x = [-1, 0, 1, -1, 1, -1, 0, 1]
directions_y = [-1, -1, -1, 0, 0, 1, 1, 1]


def count_adjacent_occupied(seat_index, seats_double_array):
    (x, y) = seat_index
    occupied_seat_count = 0
    for direction in range(8):
        if is_seat_occupied((x + directions_x[direction], y + directions_y[direction]), seats_double_array):
            occupied_seat_count += 1

    return occupied_seat_count


def count_nearest_occupied(seat_index, seats_double_array):
    (x, y) = seat_index
    occupied_seat_count = 0
    for direction in range(8):
        direction_x = x + directions_x[direction]
        direction_y = y + directions_y[direction]
        while not seat_exists((direction_x, direction_y), seats_double_array):
            direction_x += directions_x[direction]
            direction_y += directions_y[direction]
        if is_seat_occupied((direction_x, direction_y), seats_double_array):
            occupied_seat_count += 1

    return occupied_seat_count


def seat_exists(seat_index, seats_double_array):
    (x, y) = seat_index
    if 0 <= y < len(seats_double_array):
        seats_row = seats_double_array[y]
        if 0 <= x < len(seats_row):
            if seats_row[x] == ".":
                return False
    return True


def is_seat_occupied(seat_index, seats_double_array):
    (x, y) = seat_index
    if 0 <= y < len(seats_double_array):
        seats_row = seats_double_array[y]
        if 0 <= x < len(seats_row):
            if seats_row[x] == "#":
                return True
    return False


def day11():
    seats = []
    with open(os.path.join(sys.path[0], "inputs/input_day11.txt"), "r") as file:
        for line in file:
            row_values = []
            row = line.rstrip()
            row_length = len(row)
            for seat in row:
                row_values.append(seat)
            seats.append(row_values)

    old_seat_map = copy.deepcopy(seats)
    new_seat_map = copy.deepcopy(seats)
    seat_changed_status = True
    while seat_changed_status:
        occupied_seats = 0
        seat_changed_status = False
        for row in range(len(old_seat_map)):
            for seat in range(row_length):
                if old_seat_map[row][seat] != '.':
                    adjacent_occupied = count_adjacent_occupied((seat, row), old_seat_map)
                    if old_seat_map[row][seat] == '#' and adjacent_occupied > 3:
                        new_seat_map[row][seat] = "L"
                        seat_changed_status = True
                    elif old_seat_map[row][seat] == 'L' and adjacent_occupied == 0:
                        new_seat_map[row][seat] = '#'
                        seat_changed_status = True
                    else:
                        new_seat_map[row][seat] = old_seat_map[row][seat]
                    if new_seat_map[row][seat] == '#':
                        occupied_seats += 1
        old_seat_map = copy.deepcopy(new_seat_map)

    print("Solution part1: " + str(occupied_seats))

    timing.log("Part 1 finished!")

    old_seat_map = copy.deepcopy(seats)
    new_seat_map = copy.deepcopy(seats)
    seat_changed_status = True
    while seat_changed_status:
        occupied_seats = 0
        seat_changed_status = False
        for row in range(len(old_seat_map)):
            for seat in range(row_length):
                if old_seat_map[row][seat] != '.':
                    adjacent_occupied = count_nearest_occupied((seat, row), old_seat_map)
                    if old_seat_map[row][seat] == '#' and adjacent_occupied > 4:
                        new_seat_map[row][seat] = "L"
                        seat_changed_status = True
                    elif old_seat_map[row][seat] == 'L' and adjacent_occupied == 0:
                        new_seat_map[row][seat] = '#'
                        seat_changed_status = True
                    else:
                        new_seat_map[row][seat] = old_seat_map[row][seat]
                    if new_seat_map[row][seat] == '#':
                        occupied_seats += 1
        old_seat_map = copy.deepcopy(new_seat_map)

    print("Solution part2: " + str(occupied_seats))
