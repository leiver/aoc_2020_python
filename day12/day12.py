import tools.timing
import os
import sys

def day12():
    commands = []
    direction_y = [0, 1, 0, -1]
    direction_x = [1, 0, -1, 0]
    directions = {"E": 0, "S": 1, "W": 2, "N": 3}
    rotation = [1, -1, -1]
    part1_direction = part1_x = part1_y = 0
    boat_x = boat_y = 0
    waypoint_x = 10
    waypoint_y = -1
    with open(os.path.join(sys.path[0], "day12/input_day12.txt"), "r") as file:
        for line in file:
            command = line[0]
            amount = int(line.rstrip()[1:])
            #print(line)
            commands.append((command, amount))
            if command == "R":
                part1_direction = int((part1_direction + (amount / 90)) % 4)

                rotation_index = int(amount / 90) - 1
                waypoint_x *= rotation[rotation_index]
                waypoint_y *= rotation[::-1][rotation_index]
                if rotation_index != 1:
                    waypoint_temp = waypoint_x
                    waypoint_x = waypoint_y
                    waypoint_y = waypoint_temp
            elif command == "L":
                part1_direction = int((part1_direction + 4 - (amount / 90)) % 4)

                rotation_index = int(amount / 90) - 1
                waypoint_x *= rotation[::-1][rotation_index]
                waypoint_y *= rotation[rotation_index]
                if rotation_index != 1:
                    waypoint_temp = waypoint_x
                    waypoint_x = waypoint_y
                    waypoint_y = waypoint_temp
            elif command == "F":
                part1_x += direction_x[part1_direction] * amount
                part1_y += direction_y[part1_direction] * amount

                boat_x += waypoint_x * amount
                boat_y += waypoint_y * amount
            elif command in directions:
                part1_x += direction_x[directions[command]] * amount
                part1_y += direction_y[directions[command]] * amount

                waypoint_x += direction_x[directions[command]] * amount
                waypoint_y += direction_y[directions[command]] * amount
            #print("waypoint x,y = " + str(waypoint_x) + "," + str(waypoint_y))
            #print("boat x,y = " + str(boat_x) + "," + str(boat_y))
            #input()

    print("Solution part1: " + str(abs(part1_x) + abs(part1_y)))

    print("Solution part2: " + str(abs(boat_x) + abs(boat_y)))
