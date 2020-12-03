import timing
import os
import sys

def part1():

    x_max = 0
    y_max = 0

    map = {}

    x = 0
    y = 0


    with open(os.path.join(sys.path[0], "input_day3.txt"), "r") as file:
        for line in file:
            for char in line.strip():
                map[(x,y)] = char
                x+=1
                if x > x_max:
                    x_max = x
            x=0
            y+=1
            if y > y_max:
                y_max = y

    trees_1 = 0
    trees_2 = 0
    trees_3 = 0
    trees_4 = 0
    trees_5 = 0
    x_1 = 0
    x_2 = 0
    x_3 = 0
    x_4 = 0
    x_5 = 0
    for y in range(1,y_max):
        x_1 = (x_1+1) % x_max
        if map[(x_1,y)] == '#':
            trees_1 += 1
        x_2 = (x_2+3) % x_max
        if map[(x_2,y)] == '#':
            trees_2 += 1
        x_3 = (x_3+5) % x_max
        if map[(x_3,y)] == '#':
            trees_3 += 1
        x_4 = (x_4+7) % x_max
        if map[(x_4,y)] == '#':
            trees_4 += 1
        if y % 2 == 0:
            x_5 = (x_5+1) % x_max
            if map[(x_5,y)] == '#':
                trees_5 += 1

    print("Solution 1: ", trees_2)

    print("solution 2: ", trees_1 * trees_2 * trees_3 * trees_4 * trees_5)

part1()