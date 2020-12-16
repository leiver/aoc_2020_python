from tools import timing
import os
import sys


def day16():

    rule_map = {}
    range_list = []

    invalid_fields = []
    valid_tickets = []
    with open(os.path.join(sys.path[0], "inputs/input_day16.txt"), "r") as file:
        (rules, my_ticket, tickets) = file.read().split("\n\n")
        for rule in rules.rstrip().split("\n"):
            (command, ranges) = rule.rstrip().split(": ")
            rule_map[command] = [tuple([int(bound) for bound in range_rule.split("-")]) for range_rule in ranges.split(" or ")]
            range_list.extend(rule_map[command])

        my_ticket = [int(value) for value in my_ticket.rstrip().split("\n")[1].rstrip().split(",")]
        valid_tickets.append(my_ticket)

        for ticket in tickets.rstrip().split("\n")[1:]:
            valid_ticket = True
            for value in ticket.rstrip().split(","):
                value = int(value)
                invalid = True
                for (lower_end, upper_end) in range_list:
                    if lower_end <= value <= upper_end:
                        invalid = False
                        break
                if invalid:
                    invalid_fields.append(value)
                    valid_ticket = False
            if valid_ticket:
                valid_tickets.append([int(value) for value in ticket.rstrip().split(",")])

    print("Solution part1: ", sum(invalid_fields))

    timing.log("Part 1 finished!")

    valid_index_for_rule = {}
    not_valid_index_for_rule = {}
    for ticket in valid_tickets:
        for ticket_index in range(len(ticket)):
            ticket_value = ticket[ticket_index]
            for field_name in rule_map.keys():
                valid_for_field = False
                for (lower_end, upper_end) in rule_map[field_name]:
                    if lower_end <= ticket_value <= upper_end:
                        valid_for_field = True
                if valid_for_field and (field_name not in not_valid_index_for_rule or ticket_index not in not_valid_index_for_rule[field_name]):
                    if field_name in valid_index_for_rule:
                        valid_index_for_rule[field_name].add(ticket_index)
                    else:
                        valid_index_for_rule[field_name] = {ticket_index}
                elif not valid_for_field:
                    if field_name in valid_index_for_rule and ticket_index in valid_index_for_rule[field_name]:
                        valid_index_for_rule[field_name].remove(ticket_index)
                    if field_name in not_valid_index_for_rule:
                        not_valid_index_for_rule[field_name].add(ticket_index)
                    else:
                        not_valid_index_for_rule[field_name] = {ticket_index}

    valid_index_for_rule_sorted_list = list(valid_index_for_rule.items())
    valid_index_for_rule_sorted_list.sort(key=sorting)

    departure_fields = []
    solution_part_2 = 1
    known_indexes = []
    while len(departure_fields) < 6:
        for (field_name, indexes) in valid_index_for_rule_sorted_list:
            filtered_indexes = [index for index in indexes if index not in known_indexes]
            if len(filtered_indexes) == 1:
                known_indexes.append(filtered_indexes[0])
                if field_name.startswith("departure"):
                    departure_fields.append(filtered_indexes[0])
                    solution_part_2 *= my_ticket[filtered_indexes[0]]

    print("Solution part2: ", solution_part_2)


def sorting(item):
    (_, list_to_length) = item
    return len(list_to_length)
