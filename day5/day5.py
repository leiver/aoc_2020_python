import os
import sys

highest_id = 0
seat_map = {}
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

        if 0 < row_value < 127 and 0 < column_value < 7:
            # print("added to seatmap " + str(row_value) + ", " + str(column_value))
            seat_map[(row_value, column_value)] = 1

        seat_id = (row_value * 8) + column_value
        if seat_id > highest_id:
            highest_id = seat_id

print("solution part1: " + str(highest_id))

for row in range(8,117):
    for column in range():
        if (row, column) not in seat_map.keys():
            print("solution part2: " + str((row * 8) + column) + " at: " + str(row) + ", " + str(column))





# BFFFBBF RRR: row 70, column 7, seat ID 567.
# FFFBBBF RRR: row 14, column 7, seat ID 119.
# BBFFBBF RLL: row 102, column 4, seat ID 820.