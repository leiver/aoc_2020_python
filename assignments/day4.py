from tools import timing
import os
import sys
import re


def validate_key_value_pair(passport_key, passport_value):
    if passport_key == "byr":
        return len(passport_value) == 4 and passport_value.isnumeric() and 1920 <= int(passport_value) <= 2002
    if passport_key == "iyr":
        return len(passport_value) == 4 and passport_value.isnumeric() and 2010 <= int(passport_value) <= 2020
    if passport_key == "eyr":
        return len(passport_value) == 4 and passport_value.isnumeric() and 2020 <= int(passport_value) <= 2030
    if passport_key == "hgt":
        number = passport_value[0:len(passport_value) - 2]
        return number.isnumeric() and (
                (passport_value.endswith("cm") and 150 <= int(number) <= 193) or
                (passport_value.endswith("in") and 59 <= int(number) <= 76)
        )
    if passport_key == "hcl":
        return re.compile("^#[0-9a-f]{6}$").match(passport_value)
    if passport_key == "ecl":
        return re.compile("^(amb|blu|brn|gry|grn|hzl|oth)$").match(passport_value)
    if passport_key == "pid":
        return re.compile("^[0-9]{9}$").match(passport_value)
    return True


def day4():
    required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

    valid_passports_part_1 = valid_passports_part_2 = 0

    with open(os.path.join(sys.path[0], "inputs/input_day4.txt"), "r") as file:
        for passport in file.read().split("\n\n"):
            keys = []
            valid_part_2 = True
            for key_value in passport.replace("\n", " ").split(" "):
                key_value = key_value.split(":")
                key = key_value[0]
                value = ""
                if len(key_value) > 1:
                    value = key_value[1]
                keys.append(key)
                if not validate_key_value_pair(key, value):
                    valid_part_2 = False

            if valid_part_2 and all(item in keys for item in required_fields):
                valid_passports_part_2 += 1
            if all(item in keys for item in required_fields):
                valid_passports_part_1 += 1

    print("solution part 1: " + str(valid_passports_part_1))
    print("solution part 2: " + str(valid_passports_part_2))
