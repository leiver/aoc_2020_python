import timing
import os
import sys
import re

def validateKeyValuePair(key, value):
    if key == "byr":
        return len(value) == 4 and value.isnumeric() and 1920 <= int(value) <= 2002
    if key == "iyr":
        return len(value) == 4 and value.isnumeric() and 2010 <= int(value) <= 2020
    if key == "eyr":
        return len(value) == 4 and value.isnumeric() and 2020 <= int(value) <= 2030
    if key == "hgt":
        number = value[0:len(value)-2]
        return number.isnumeric() and ((value.endswith("cm") and 150 <= int(number) <= 193) or (value.endswith("in") and 59 <= int(number) <= 76))
    if key == "hcl":
        return re.compile("^#[0-9a-f]{6}$").match(value)
    if key == "ecl":
        return re.compile("^(amb|blu|brn|gry|grn|hzl|oth)$").match(value)
    if key == "pid":
        return re.compile("^[0-9]{9}$").match(value)
    return True

required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

valid_passports_part_1 = valid_passports_part_2 = 0

with open(os.path.join(sys.path[0], "input_day4.txt"), "r") as file:
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
            if not validateKeyValuePair(key, value):
                valid_part_2 = False

        if valid_part_2 and all(item in keys for item in required_fields):
            valid_passports_part_2 += 1
        if all(item in keys for item in required_fields):
            valid_passports_part_1 += 1

print("solution part 1: " + str(valid_passports_part_1))
print("solution part 2: " + str(valid_passports_part_2))