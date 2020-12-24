from tools import timing
import os
import sys
from collections import deque

valid_instructions = ["e", "w", "ne", "nw", "se", "sw"]


def coords_from_instruction(x, y, instruction):
    if len(instruction) == 2 and "e" in instruction and abs(y % 2) == 0:
        x += 1
    if len(instruction) == 2 and "w" in instruction and abs(y % 2) == 1:
        x -= 1
    if instruction == "e":
        x += 1
    if instruction == "w":
        x -= 1
    if "s" in instruction:
        y += 1
    if "n" in instruction:
        y -= 1
    return x, y


def get_neighbours(x, y, floor_map):
    neighbours = []
    black_tile_count = 0
    for instruction in valid_instructions:
        coords = coords_from_instruction(x, y, instruction)
        if coords in floor_map:
            black_tile_count += 1
        neighbours.append(coords)
    return black_tile_count, neighbours


def day24():
    floor_map = set()
    paths = []
    with open(os.path.join(sys.path[0], "inputs/input_day24.txt"), "r") as file:
        for path in file:
            instructions = []
            x = y = 0
            path = path.rstrip()
            path_iter = iter(path)
            instruction = next(path_iter, None)
            while instruction:
                if instruction in ["n", "s"]:
                    instruction += next(path_iter)

                instructions.append(instruction)

                (x, y) = coords_from_instruction(x, y, instruction)

                instruction = next(path_iter, None)

            if (x, y) in floor_map:
                floor_map.remove((x, y))
            else:
                floor_map.add((x, y))

            paths.append(instructions)

    print("Solution part1:", len(floor_map))

    timing.log("Part 1 finished!")

    for _ in range(100):
        new_floor = set()
        white_tiles_parsed = set()
        for (x, y) in floor_map:
            (black_tile_count, neighbours) = get_neighbours(x, y, floor_map)
            if 0 < black_tile_count <= 2:
                new_floor.add((x, y))
            for neighbour in neighbours:
                if neighbour not in floor_map and neighbour not in white_tiles_parsed:
                    (black_tile_count, _) = get_neighbours(neighbour[0], neighbour[1], floor_map)
                    if black_tile_count == 2:
                        new_floor.add(neighbour)
                    white_tiles_parsed.add(neighbour)
        floor_map = new_floor

    print("Solution part2:", len(floor_map))
