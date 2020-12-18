from tools import timing
import os
import sys
import copy


def get_neighbours(dimension_map, coordinates):
    (x, y, z) = coordinates
    neighbours = []
    boxes = 0
    for neighbor_x in range(x - 1, x + 2):
        for neighbor_y in range(y - 1, y + 2):
            for neighbor_z in range(z - 1, z + 2):
                if x != neighbor_x or y != neighbor_y or z != neighbor_z:
                    neighbour_coordinates = (neighbor_x, neighbor_y, neighbor_z)
                    neighbours.append(neighbour_coordinates)
                    if neighbour_coordinates in dimension_map:
                        boxes += 1
    return boxes, neighbours


def get_4d_neighbours(dimension_map, coordinates):
    (x, y, z, w) = coordinates
    neighbours = []
    boxes = 0
    for neighbor_x in range(x - 1, x + 2):
        for neighbor_y in range(y - 1, y + 2):
            for neighbor_z in range(z - 1, z + 2):
                for neighbor_w in range(w - 1, w + 2):
                    if x != neighbor_x or y != neighbor_y or z != neighbor_z or w != neighbor_w:
                        neighbour_coordinates = (neighbor_x, neighbor_y, neighbor_z, neighbor_w)
                        neighbours.append(neighbour_coordinates)
                        if neighbour_coordinates in dimension_map:
                            boxes += 1
    return boxes, neighbours


def parse_box_value(box, neighbour_boxes):
    if box == "#" and (2 == neighbour_boxes or 3 == neighbour_boxes):
        return "#"
    if box == "." and neighbour_boxes == 3:
        return "#"
    return "."


def day17():
    dimension_map = {}
    four_dimension_map = {}

    with open(os.path.join(sys.path[0], "inputs/input_day17.txt"), "r") as file:
        y = 0
        for line in file:
            x = 0
            for box in line.rstrip():
                if box == "#":
                    dimension_map[(x, y, 0)] = "#"
                    four_dimension_map[(x, y, 0, 0)] = "#"
                x += 1
            y += 1

    for _ in range(6):
        next_iteration = {}
        memo = set()
        for (coordinates, box) in dimension_map.items():
            (boxes, neighbours) = get_neighbours(dimension_map, coordinates)
            new_box = parse_box_value(box, boxes)
            if new_box == "#":
                next_iteration[coordinates] = new_box
            memo.add(coordinates)

            for neighbour in neighbours:
                if neighbour not in memo:
                    (boxes, _) = get_neighbours(dimension_map, neighbour)
                    neighbour_box = "."
                    if neighbour in dimension_map:
                        neighbour_box = dimension_map[neighbour]
                    new_neighbour_box = parse_box_value(neighbour_box, boxes)
                    if new_neighbour_box == "#":
                        next_iteration[neighbour] = new_neighbour_box
                    memo.add(neighbour)
        dimension_map = copy.deepcopy(next_iteration)

    print("Solution part1: ", len(dimension_map))

    timing.log("Part 1 finished!")

    for _ in range(6):
        next_iteration = {}
        memo = set()
        for (coordinates, box) in four_dimension_map.items():
            (boxes, neighbours) = get_4d_neighbours(four_dimension_map, coordinates)
            new_box = parse_box_value(box, boxes)
            if new_box == "#":
                next_iteration[coordinates] = new_box
            memo.add(coordinates)

            for neighbour in neighbours:
                if neighbour not in memo:
                    (boxes, _) = get_4d_neighbours(four_dimension_map, neighbour)
                    neighbour_box = "."
                    if neighbour in four_dimension_map:
                        neighbour_box = four_dimension_map[neighbour]
                    new_neighbour_box = parse_box_value(neighbour_box, boxes)
                    if new_neighbour_box == "#":
                        next_iteration[neighbour] = new_neighbour_box
                    memo.add(neighbour)
        four_dimension_map = copy.deepcopy(next_iteration)

    print("Solution part2: ", len(four_dimension_map))
