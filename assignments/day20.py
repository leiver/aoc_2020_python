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
        self.pixels = [pixel_row[1:-1] for pixel_row in pixels][1:-1]
        self.pixels_with_borders = pixels

    def border_from_direction(self, direction):
        return self.borders[self.directions[direction]]

    def direction_that_matches(self, border_to_match):
        for i in range(4):
            if border_to_match in self.borders[i]:
                return self.directions_other_way[i]
        return None

    def transmute_to_match(self, direction, border_to_match):
        matched_direction = self.direction_that_matches(border_to_match)
        if matched_direction:
            matched_border = self.border_from_direction(matched_direction)
            if matched_border[0] == border_to_match:
                if matched_direction in ["N", "S"]:
                    self.flip_x()
                else:
                    self.flip_y()
            rotation = (self.directions[matched_direction] + 4 - self.directions[direction]) % 4
            if direction == matched_direction or direction == self.opposite_direction[matched_direction]:
                rotation = (rotation + 2) % 4
            self.rotate(rotation)
            return True
        return False

    def rotate(self, times_with_clock):
        if times_with_clock % 4 == 0:
            return
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
                    pixel_row.append(self.pixels[(x * -1) - 1][y])
                if times_with_clock == 2:
                    pixel_row.append(self.pixels[(y * -1) - 1][(x * -1) - 1])
                if times_with_clock == 3:
                    pixel_row.append(self.pixels[x][(y * -1) - 1])
            new_pixels.append(pixel_row)
        self.pixels = new_pixels
        new_pixels = []
        for y in range(len(self.pixels_with_borders)):
            pixel_row = []
            for x in range(len(self.pixels_with_borders)):
                if times_with_clock == 1:
                    pixel_row.append(self.pixels_with_borders[(x * -1) - 1][y])
                if times_with_clock == 2:
                    pixel_row.append(self.pixels_with_borders[(y * -1) - 1][(x * -1) - 1])
                if times_with_clock == 3:
                    pixel_row.append(self.pixels_with_borders[x][(y * -1) - 1])
            new_pixels.append(pixel_row)
        self.pixels_with_borders = new_pixels

    def flip_y(self):
        for i in range(4):
            (border, reverse_border) = self.borders[i]
            self.borders[i] = (reverse_border, border)
        self.north_border = self.borders[2]
        self.east_border = self.borders[1]
        self.south_border = self.borders[0]
        self.west_border = self.borders[3]
        self.borders[0] = self.north_border
        self.borders[2] = self.south_border
        self.pixels = self.pixels[::-1]
        self.pixels_with_borders = self.pixels_with_borders[::-1]

    def flip_x(self):
        for i in range(4):
            (border, reverse_border) = self.borders[i]
            self.borders[i] = (reverse_border, border)
        self.north_border = self.borders[0]
        self.east_border = self.borders[3]
        self.south_border = self.borders[2]
        self.west_border = self.borders[1]
        self.borders[1] = self.east_border
        self.borders[3] = self.west_border
        self.pixels = [pixel_row[::-1] for pixel_row in self.pixels]
        self.pixels_with_borders = [pixel_row[::-1] for pixel_row in self.pixels_with_borders]

    def __repr__(self):
        return f"Picture:\n\tPicture_id: {self.picture_id}\n\tnorth_border: {self.north_border}\n\teast_border: {self.east_border}\n\tsouth_border: {self.south_border}\n\twest_border: {self.west_border}\n"

    def __str__(self):
        return f"Picture:\n\tPicture_id: {self.picture_id}\n\tnorth_border: {self.north_border}\n\teast_border: {self.east_border}\n\tsouth_border: {self.south_border}\n\twest_border: {self.west_border}\n"


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

            north_border_pixels = image_lines[0]
            north_border = parse_binary_from_border(north_border_pixels)
            north_border_reverse = parse_binary_from_border(north_border_pixels[::-1])
            add_to_images_from_border_map(images_from_border, north_border, image_id)
            add_to_images_from_border_map(images_from_reverse_border, north_border_reverse, image_id)

            east_border_pixels = "".join([pixels[-1] for pixels in image_lines])
            east_border = parse_binary_from_border(east_border_pixels)
            east_border_reverse = parse_binary_from_border(east_border_pixels[::-1])
            add_to_images_from_border_map(images_from_border, east_border, image_id)
            add_to_images_from_border_map(images_from_reverse_border, east_border_reverse, image_id)

            south_border_pixels = image_lines[-1]
            south_border = parse_binary_from_border(south_border_pixels[::-1])
            south_border_reverse = parse_binary_from_border(south_border_pixels)
            add_to_images_from_border_map(images_from_border, south_border, image_id)
            add_to_images_from_border_map(images_from_reverse_border, south_border_reverse, image_id)

            west_border_pixels = "".join([pixels[0] for pixels in image_lines[::-1]])
            west_border = parse_binary_from_border(west_border_pixels)
            west_border_reverse = parse_binary_from_border(west_border_pixels[::-1])
            add_to_images_from_border_map(images_from_border, west_border, image_id)
            add_to_images_from_border_map(images_from_reverse_border, west_border_reverse, image_id)

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
                "E": (east_border, east_border_reverse),
                "S": (south_border, south_border_reverse),
                "W": (west_border, west_border_reverse)
            }

    total_amount_of_images = len(image_borders)

    directions = {"N": 0, "E": 1, "S": 2, "W": 3}
    directions_other_way = {0: "N", 1: "E", 2: "S", 3: "W"}
    direction_x = {"N": 0, "E": 1, "S": 0, "W": -1}
    direction_y = {"N": -1, "E": 0, "S": 1, "W": 0}
    opposite_direction = {"N": "S", "E": "W", "S": "N", "W": "E"}

    open_borders = {}
    full_image = {}
    full_picture_length = int(math.sqrt(len(images)))
    for (image_id, picture) in images.items():
        borders_matched = []
        for i in range(4):
            (border, _) = picture.border_from_direction(directions_other_way[i])
            if len(images_from_border[border]) == 2 or border in images_from_reverse_border:
                borders_matched.append(i)
        if len(borders_matched) == 2:
            rotation = (borders_matched[0] - borders_matched[1] + 4) % 4
            if rotation == 1:
                left_most_border = borders_matched[1]
            elif rotation == 3:
                left_most_border = borders_matched[0]
            picture.rotate((1 - left_most_border + 4) % 4)
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
            image_to_match_border_x = x + direction_x[direction]
            image_to_match_border_y = y + direction_y[direction]
            matching_images = 0
            if 0 <= image_to_match_border_x < full_picture_length and 0 <= image_to_match_border_y < full_picture_length:
                matching_border_found = False
                for image_to_match in images.values():
                    if image_to_match not in full_image.values():
                        if image_to_match.direction_that_matches(border[0]):
                            all_directions_match = True
                            for direction_matcher in directions.keys():
                                if (
                                        image_to_match_border_x + direction_x[direction_matcher],
                                        image_to_match_border_y + direction_y[direction_matcher],
                                        opposite_direction[direction_matcher]
                                ) in open_borders and not image_to_match.direction_that_matches(open_borders[(
                                        image_to_match_border_x + direction_x[direction_matcher],
                                        image_to_match_border_y + direction_y[direction_matcher],
                                        opposite_direction[direction_matcher]
                                )][0]):
                                    all_directions_match = False
                                    break

                            if all_directions_match:
                                matching_image = image_to_match
                                matching_images += 1
                if matching_images == 1:
                    matching_image.transmute_to_match(direction, border[0])
                    full_image[(image_to_match_border_x, image_to_match_border_y)] = matching_image
                    matching_border_found = True
                    break
        if matching_border_found:
            for direction in directions.keys():
                opposing_border_x = image_to_match_border_x + direction_x[direction]
                opposing_border_y = image_to_match_border_y + direction_y[direction]
                opposing_border = (opposing_border_x, opposing_border_y, opposite_direction[direction])
                if opposing_border in open_borders:
                    del open_borders[opposing_border]
                elif 0 <= opposing_border_x < full_picture_length and 0 <= opposing_border_y < full_picture_length:
                    open_borders[(image_to_match_border_x, image_to_match_border_y, direction)] = matching_image.border_from_direction(direction)

    solution_part1 = full_image[(0, 0)].picture_id * full_image[(0, full_picture_length-1)].picture_id * full_image[(full_picture_length-1, 0)].picture_id * full_image[(full_picture_length-1, full_picture_length-1)].picture_id

    print("Solution part1: ", solution_part1)

    timing.log("Part 1 finished!")

    pixels = []
    for picture_y in range(full_picture_length):
        for picture_x in range(full_picture_length):
            if picture_x == 0:
                pixels.extend(full_image[(picture_x, picture_y)].pixels)
            else:
                pixels_from_picture = full_image[(picture_x, picture_y)].pixels
                for pixel_y in range(len(pixels_from_picture)):
                    pixels[(picture_y * len(pixels_from_picture)) + pixel_y].extend(pixels_from_picture[pixel_y])

    full_picture = Picture(1, (0, 0), (0, 0), (0, 0), (0, 0), pixels)

    nessy = [(0, 1), (1, 2), (4, 2), (5, 1), (6, 1), (7, 2), (10, 2), (11, 1), (12, 1), (13, 2), (16, 2), (17, 1), (18, 0), (18, 1), (19, 1)]

    full_picture_length = len(full_picture.pixels_with_borders)

    nessy_orientation = False
    rotation_count = 0
    flipped_x = False
    flipped_y = False
    nessys_found = 0
    while not nessy_orientation:
        modified_picture = copy.deepcopy(full_picture.pixels_with_borders)
        for y in range(full_picture_length-2):
            for x in range(full_picture_length-19):
                nessy_found = True
                for nessy_coord in nessy:
                    if full_picture.pixels_with_borders[y + nessy_coord[1]][x + nessy_coord[0]] != "#":
                        nessy_found = False
                        break
                if nessy_found:
                    nessys_found += 1
                    nessy_orientation = True
                    for nessy_coord in nessy:
                        modified_picture[y + nessy_coord[1]][x + nessy_coord[0]] = "O"
        if not nessy_orientation:
            if rotation_count == 3 and not flipped_x:
                full_picture.flip_x()
                rotation_count = 0
                flipped_x = True
            elif rotation_count == 3 and not flipped_y:
                full_picture.flip_y()
                rotation_count = 0
                flipped_y = True
            elif rotation_count == 3:
                break
            else:
                full_picture.rotate(1)
                rotation_count += 1

    rough_water_count = 0
    for y in range(full_picture_length):
        for x in range(full_picture_length):
            if modified_picture[y][x] == "#":
                rough_water_count += 1

    print("Solution part2: ", rough_water_count)
