from tools import timing
import os
import sys
import copy


def is_input_valid(message, rule_map, index, rule):
    if index >= len(message):
        return 0
    for rule_option in rule_map[rule]:
        current_index = index
        for rule_to_parse in rule_option:
            if rule_to_parse.isnumeric():
                current_index = is_input_valid(message, rule_map, current_index, int(rule_to_parse))
                if not current_index:
                    break
            elif message[index] == rule_to_parse:
                return index + 1
            else:
                return 0
        if current_index:
            return current_index
    return current_index


def create_regex(rule_map, rule):
    options = rule_map[rule]
    result = ""
    if len(options) > 1:
        result += "("
    first_option = True
    for rule_option in rule_map[rule]:
        if not first_option:
            result += "|"
        if str(rule) in rule_option:
            result += "("
        for rule_in_option in rule_option:
            if rule_in_option.isnumeric():
                result += create_regex(rule_map, int(rule_in_option))
            else:
                return rule_in_option
        if rule in rule_option:
            result += ")+"
        first_option = False
    if len(options) > 1:
        result += ")"
    return result


def day19():
    rule_map = {}

    with open(os.path.join(sys.path[0], "inputs/input_day19.txt"), "r") as file:
        (rules, messages) = file.read().split("\n\n")
        for rule in rules.rstrip().split("\n"):
            (rule_id, sub_rules) = rule.rstrip().split(": ")
            rule_map[int(rule_id)] = [
                [sub_rule_element.strip("\"") for sub_rule_element in sub_rule.split(" ")]
                for sub_rule in sub_rules.split(" | ")
            ]

        valid_messages = 0
        for message in messages.rstrip().split("\n"):
            message = message.rstrip()
            valid_to_index = is_input_valid(message, rule_map, 0, 0)
            if valid_to_index == (len(message)):
                valid_messages += 1
        print("Solution part1: ", valid_messages)

        timing.log("Part 1 finished!")

        valid_messages = 0

        for message in messages.rstrip().split("\n"):
            message = message.rstrip()
            forty_two_looped = 0
            forty_two_success = True
            valid_to_index = 0
            while forty_two_success:
                new_index = is_input_valid(message, rule_map, valid_to_index, 42)
                if new_index:
                    valid_to_index = new_index
                    forty_two_looped += 1
                else:
                    forty_two_success = False
            thirty_one_looped = 0
            thirty_one_success = True
            while thirty_one_success:
                new_index = is_input_valid(message, rule_map, valid_to_index, 31)
                if new_index:
                    valid_to_index = new_index
                    thirty_one_looped += 1
                else:
                    thirty_one_success = False

            if forty_two_looped > thirty_one_looped > 0 and valid_to_index == len(message):
                valid_messages += 1

        print("Solution part2: ", valid_messages)

