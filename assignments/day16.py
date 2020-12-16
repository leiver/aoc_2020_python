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
                    #print(field_name, " = ", lower_end, ", ", upper_end, ": ", ticket_value)
                    if lower_end <= ticket_value <= upper_end:
                        valid_for_field = True
                #print("    ", valid_for_field)
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
                #print(valid_index_for_rule)
                #print(not_valid_index_for_rule)


    print(valid_index_for_rule)
    print()
    print(not_valid_index_for_rule)
    solution_part_2 = 1
    for field_name in valid_index_for_rule.keys():
        if field_name.startswith("departure"):
            field_index = valid_index_for_rule[field_name]
            solution_part_2 *= my_ticket[field_index]

    print("Solution part2: ", solution_part_2)
