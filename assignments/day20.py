from tools import timing
import os
import sys

# '{0:036b}'.format(int(value))


def parse_binary_from_border(border):
    binary = ""
    for pixel in border:
        if pixel == "#":
            binary += "1"
        elif pixel == ".":
            binary += "0"
    return int(binary, 2)


def add_to_images_from_border_map(images_from_border, border, image_id):
    if border in images_from_border:
        images_from_border[border].append(image_id)
    else:
        images_from_border[border] = [image_id]


def day20():

    image_borders = {}
    images_from_border = {}
    images_from_reverse_border = {}
    with open(os.path.join(sys.path[0], "inputs/input_day20.txt"), "r") as file:
        for image in file.read().rstrip().split("\n\n"):
            image_lines = image.rstrip().split("\n")
            image_id = int(image_lines[0][5:].strip(":"))
            image_lines = image_lines[1:]
            dimension = len(image_lines[0])

            north_border_pixels = image_lines[0]
            north_border = parse_binary_from_border(north_border_pixels)
            north_border_reverse = parse_binary_from_border(north_border_pixels[::-1])
            add_to_images_from_border_map(images_from_border, north_border, image_id)
            add_to_images_from_border_map(images_from_reverse_border, north_border_reverse, image_id)

            west_border_pixels = "".join([pixels[dimension-1] for pixels in image_lines])
            west_border = parse_binary_from_border(west_border_pixels)
            west_border_reverse = parse_binary_from_border(west_border_pixels[::-1])
            add_to_images_from_border_map(images_from_border, west_border, image_id)
            add_to_images_from_border_map(images_from_reverse_border, west_border_reverse, image_id)

            south_border_pixels = image_lines[dimension-1]
            south_border = parse_binary_from_border(south_border_pixels[::-1])
            south_border_reverse = parse_binary_from_border(south_border_pixels)
            add_to_images_from_border_map(images_from_border, south_border, image_id)
            add_to_images_from_border_map(images_from_reverse_border, south_border_reverse, image_id)

            east_border_pixels = "".join([pixels[0] for pixels in image_lines][::-1])
            east_border = parse_binary_from_border(east_border_pixels)
            east_border_reverse = parse_binary_from_border(east_border_pixels[::-1])
            add_to_images_from_border_map(images_from_border, east_border, image_id)
            add_to_images_from_border_map(images_from_reverse_border, east_border_reverse, image_id)

            image_borders[image_id] = {
                "N": (north_border, north_border_reverse),
                "E": (west_border, west_border_reverse),
                "S": (south_border, south_border_reverse),
                "W": (east_border, east_border_reverse)
            }

    highest_single_match_border = 0
    for (image, borders) in image_borders.items():
        single_match_borders = 0
        for (border, _) in borders.values():
            if len(images_from_border[border]) == 1:
                single_match_borders += 1
        if single_match_borders == 4:
            image_id = image
            highest_single_match_border = 4
        if single_match_borders > highest_single_match_border:
            highest_single_match_border = single_match_borders
            image_id = image

    total_amount_of_images = len(image_borders)
    images_parsed = {(0, 0): image_id}
    unconnected_borders = {
        (0, 0, "N"): image_borders[image_id]["N"],
        (0, 0, "E"): image_borders[image_id]["E"],
        (0, 0, "S"): image_borders[image_id]["S"],
        (0, 0, "W"): image_borders[image_id]["W"]
    }

    directions = {"N": 0, "E": 1, "S": 2, "W": 3}
    directions_other_way = {0: "N", 1: "E", 2: "S", 3: "W"}
    direction_x = {"N": 0, "E": 1, "S": 0, "W": -1}
    direction_y = {"N": -1, "E": 0, "S": 1, "W": 0}
    opposite_direction = {"N": "S", "E": "W", "S": "N", "W": "E"}

    lowest_x = highest_x = lowest_y = highest_y = 0

    #print(image_borders)
    #print()
    #print(images_from_border)
    #print()
    #print(images_from_reverse_border)

    while len(images_parsed) != total_amount_of_images:
        for (border_id, border) in unconnected_borders.items():
            (x, y, direction) = border_id
            images_from_reverse = []
            if border[0] in images_from_reverse_border:
                images_from_reverse = images_from_reverse_border[border[0]]
            images = images_from_border[border[0]]
            if len(images_from_reverse) == 1 and len(images) == 1:
                image_to_add = images_from_reverse[0]
                image_to_add_x = x + direction_x[direction]
                image_to_add_y = y + direction_y[direction]
                for (image_to_add_direction, image_to_add_border) in image_borders[image_to_add].items():
                    if image_to_add_border[0] == border[1]:
                        image_to_add_rotation = (directions[image_to_add_direction] + 4 - directions[direction]) % 4
                        flipped_x = False
                        flipped_y = False
                        break
                images_parsed[(image_to_add_x, image_to_add_y)] = image_to_add
                if image_to_add_x < lowest_x:
                    lowest_x = image_to_add_x
                elif image_to_add_x > highest_x:
                    highest_x = image_to_add_x
                if image_to_add_y < lowest_y:
                    lowest_y = image_to_add_y
                elif image_to_add_y > highest_y:
                    highest_y = image_to_add_y
                break
            elif len(images) == 2 and len(images_from_reverse) == 0:
                image_to_add = [image_not_parsed for image_not_parsed in images if image_not_parsed != images_parsed[(x, y)]][0]
                image_to_add_x = x + direction_x[direction]
                image_to_add_y = y + direction_y[direction]
                for (image_to_add_direction, image_to_add_border) in image_borders[image_to_add].items():
                    if image_to_add_border[0] == border[0]:
                        if image_to_add_direction in ["N", "S"]:
                            flipped_y = True
                            flipped_x = False
                        else:
                            flipped_y = False
                            flipped_x = True

                        image_to_add_rotation = (directions[image_to_add_direction] + 6 - directions[direction]) % 4
                        break


        for (direction, borders) in image_borders[image_to_add].items():
            direction = directions_other_way[(directions[direction] + image_to_add_rotation) % 4]
            opposite_border_id = (image_to_add_x + direction_x[direction], image_to_add_y + direction_y[direction], opposite_direction[direction])
            if opposite_border_id in unconnected_borders:
                del unconnected_borders[opposite_border_id]
            else:
                unconnected_borders[(image_to_add_x, image_to_add_y, direction)] = borders

    for y in range(lowest_y, highest_y+1):
        line = ""
        for x in range(lowest_x, highest_x+1):
            if (x, y) in images_parsed:
                line += "#"
            else:
                line += "."
        #print(line)

    direction_arrow = {"N": "^", "E": ">", "S": "v", "W": "<"}
    solution_part1 = 1
    for (image, borders) in image_borders.items():
        #print(image)
        line = ""
        unmatched_directions = 0
        for (direction, (border, reverse_border)) in borders.items():
            if border in images_from_reverse_border or len(images_from_border[border]) > 1:
                line += direction_arrow[direction]
            else:
                unmatched_directions += 1
                line += "x"
        if unmatched_directions == 2:
            solution_part1 *= image
        #print(line)
        #print()

    #print(len(images_parsed))

    print("Solution part1: ", solution_part1)
