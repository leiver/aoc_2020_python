from tools import timing
import os
import sys
import copy
import math


class Picture:
    directions = {"N": 0, "E": 1, "S": 2, "W": 3}
    directions_other_way = {0: "N", 1: "E", 2: "S", 3: "W"}
    opposite_direction = {"N": "S", "E": "W", "S": "N", "W": "E"}

    def __init__(
            self,
            picture_id,
            north_border,
            east_border,
            south_border,
            west_border,
            pixels
    ):
        self.picture_id = picture_id
        self.north_border = north_border
        self.east_border = east_border
        self.south_border = south_border
        self.west_border = west_border
        self.borders = [north_border, east_border, south_border, west_border]
        self.pixels = pixels

    def border_from_direction(self, direction):
        return self.borders[self.directions[direction]]

    def direction_that_matches(self, border_to_match):
        for i in range(4):
            if border_to_match in self.borders[i]:
                return self.directions_other_way[i]

    def transmute_to_match(self, direction, border_to_match):
        matched_direction = self.direction_that_matches(border_to_match)
        if matched_direction:
            matched_border = self.border_from_direction(matched_direction)
            if matched_border[0] == border_to_match:
                if matched_direction in ["N", "S"]:
                    self.flip_x()
                else:
                    self.flip_y()
            self.rotate((self.directions[matched_direction] + 4 - self.directions[direction]) % 4)
            return True
        return False

    def rotate(self, times_with_clock):
        copy_of_borders = copy.deepcopy(self.borders)
        for i in range(4):
            self.borders[(i + times_with_clock) % 4] = copy_of_borders[i]
        self.north_border = self.borders[0]
        self.east_border = self.borders[1]
        self.south_border = self.borders[2]
        self.west_border = self.borders[3]
        new_pixels = []
        for y in range(len(self.pixels)):
            pixel_row = []
            for x in range(len(self.pixels)):
                if times_with_clock == 1:
                    pixel_row.append(self.pixels[x * -1][y])
                if times_with_clock == 2:
                    print(len(self.pixels))
                    print(len(self.pixels[0]))
                    print(y)
                    print(x)
                    print()
                    pixel_row.append(self.pixels[y * -1][x * -1])
                if times_with_clock == 3:
                    pixel_row.append(self.pixels[x][y * -1])
            new_pixels.append(pixel_row)
        self.pixels = new_pixels

    def flip_y(self):
        for i in range(4):
            (border, reverse_border) = self.borders[i]
            self.borders[i] = (reverse_border, border)
        self.north_border = self.borders[2]
        self.east_border = self.borders[1]
        self.south_border = self.borders[0]
        self.west_border = self.borders[3]

    def flip_x(self):
        for i in range(4):
            (border, reverse_border) = self.borders[i]
            self.borders[i] = (reverse_border, border)
        self.north_border = self.borders[0]
        self.east_border = self.borders[3]
        self.south_border = self.borders[2]
        self.west_border = self.borders[1]


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

    images = {}
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

            pixels = [[pixel for pixel in pixel_row] for pixel_row in image_lines]

            images[image_id] = Picture(
                image_id,
                (north_border, north_border_reverse),
                (east_border, east_border_reverse),
                (south_border, south_border_reverse),
                (west_border, west_border_reverse),
                pixels
            )

            image_borders[image_id] = {
                "N": (north_border, north_border_reverse),
                "E": (west_border, west_border_reverse),
                "S": (south_border, south_border_reverse),
                "W": (east_border, east_border_reverse)
            }

    total_amount_of_images = len(image_borders)

    directions = {"N": 0, "E": 1, "S": 2, "W": 3}
    directions_other_way = {0: "N", 1: "E", 2: "S", 3: "W"}
    direction_x = {"N": 0, "E": 1, "S": 0, "W": -1}
    direction_y = {"N": -1, "E": 0, "S": 1, "W": 0}
    opposite_direction = {"N": "S", "E": "W", "S": "N", "W": "E"}

    open_borders = {}
    full_image = {}
    for (image_id, picture) in images.items():
        borders_matched = []
        for i in range(4):
            (border, _) = picture.border_from_direction(directions_other_way[i])
            if len(images_from_border[border]) == 2 or border in images_from_reverse_border:
                borders_matched.append(i)
        if len(borders_matched) == 2:
            picture.rotate((1 - min(borders_matched) + 4) % 4)
            open_borders = {
                (0, 0, "N"): picture.border_from_direction("N"),
                (0, 0, "E"): picture.border_from_direction("E"),
                (0, 0, "S"): picture.border_from_direction("S"),
                (0, 0, "W"): picture.border_from_direction("W")
            }
            full_image = {(0, 0): picture}
            break

    while len(full_image) != total_amount_of_images:
        for (border_id, border) in open_borders.items():
            (x, y, direction) = border_id
            image_for_border = full_image[(x, y)].picture_id
            matched_image = 0
            if border[0] in images_from_reverse_border:
                matched_image = images_from_reverse_border[border[0]][0]
            elif len(images_from_border[border[0]]) == 2:
                matched_image = [matched_image for matched_image in images_from_border[border[0]] if matched_image != image_for_border]
                matched_image = matched_image[0]

            if matched_image:
                matched_image = images[matched_image]
                matched_image.transmute_to_match(direction, border[0])
                matched_image_x = x + direction_x[direction]
                matched_image_y = y + direction_y[direction]
                full_image[(matched_image_x, matched_image_y)] = matched_image
                break
        for direction in directions.keys():
            opposing_border = (matched_image_x + direction_x[direction], matched_image_y + direction_y[direction], opposite_direction[direction])
            if opposing_border in open_borders:
                del open_borders[opposing_border]
            else:
                open_borders[(matched_image_x, matched_image_y, direction)] = matched_image.border_from_direction(direction)

    full_picture_length = int(math.sqrt(len(full_image)))

    solution_part1 = full_image[(0, 0)] * full_image[0, full_picture_length-1] * full_image[full_picture_length-1, 0] * full_image[full_picture_length-1, full_picture_length-1]

    print("Solution part1: ", solution_part1)