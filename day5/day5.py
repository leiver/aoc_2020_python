import os
import sys

highest_id = 0
seat_map = {}
almost_solution = {}
solutions = {}

with open(os.path.join(sys.path[0], "input_day5.txt"), "r") as file:
    for line in file:
        line = line.strip()
        row_code = line[6::-1]
        column_code = line[:6:-1]

        row_value = 0
        column_value = 0
        for index in range(7):
            if row_code[index] == "B":
                row_value += pow(2, index)
            if index < len(column_code) and column_code[index] == "R":
                column_value += pow(2, index)

        seat_id = (row_value * 8) + column_value

        seat_map[seat_id] = 0
        if seat_id in almost_solution:
            almost_solution.pop(seat_id)
        if seat_id in solutions:
            solutions.pop(seat_id)

        if seat_id - 1 not in seat_map:
            if seat_id - 1 not in almost_solution:
                almost_solution[seat_id - 1] = 1
            else:
                solutions[seat_id - 1] = 2

        if seat_id + 1 not in seat_map:
            if seat_id + 1 not in almost_solution:
                almost_solution[seat_id + 1] = 1
            else:
                solutions[seat_id + 1] = 2

        seat_map[seat_id] = 0
        if seat_id > highest_id:
            highest_id = seat_id

print("solution part1: " + str(highest_id))

print("solution part2: " + str(list(solutions.keys())[0]))

