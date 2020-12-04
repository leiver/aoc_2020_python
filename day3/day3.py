import timing
import os
import sys

map = {}
x_max = y_max = y = 0

with open(os.path.join(sys.path[0], "input_day3.txt"), "r") as file:
    for line in file:
        x=0
        for char in line.strip():
            map[(x,y)] = char
            x_max = x = x + 1
        y_max = y = y + 1

trees_1 = trees_2 = trees_3 = trees_4 = trees_5 = 0
for xy in range(1,y_max):
    if map[(xy % x_max,xy)] == '#':
        trees_1 += 1
    if map[((xy * 3) % x_max,xy)] == '#':
        trees_2 += 1
    if map[((xy * 5) % x_max,xy)] == '#':
        trees_3 += 1
    if map[((xy * 7) % x_max,xy)] == '#':
        trees_4 += 1
    if xy % 2 == 0 and map[((xy/2) % x_max,xy)] == '#':
        trees_5 += 1

print("Solution 1: ", trees_2)

print("solution 2: ", trees_1 * trees_2 * trees_3 * trees_4 * trees_5)
