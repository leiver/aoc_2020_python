from tools import timing
import os
import sys


def bags_that_can_contain_given_bag(bag_to_traverse, containers_for_bag_map):
    if bag_to_traverse not in containers_for_bag_map:
        return []
    bag_content = containers_for_bag_map[bag_to_traverse]
    bags_to_return = [bag_to_return for bag_to_return in bag_content]
    for (bag_in_tree) in bag_content:
        bags_to_return = \
            list(set(bags_to_return) | set(bags_that_can_contain_given_bag(bag_in_tree, containers_for_bag_map)))
    return bags_to_return


def bags_inside_given_bag(bag_to_traverse, containers_in_bag):
    bag_content = containers_in_bag[bag_to_traverse]
    bags_inside = 0
    for (amount_of_bags, bag_in_tree) in bag_content:
        if amount_of_bags != "no":
            bags_inside += \
                int(amount_of_bags) + (int(amount_of_bags) * bags_inside_given_bag(bag_in_tree, containers_in_bag))
    return bags_inside


def day7():
    bag_contents = {}
    containers_for_bag = {}
    with open(os.path.join(sys.path[0], "inputs/input_day7.txt"), "r") as file:
        for line in file:
            (bag, contents) = line.rstrip().strip(".").split(" bags contain ")
            contents = [
                (
                    value.split(" ")[0],
                    value[len(value.split(" ")[0]) + 1::].replace(" bags", "").replace(" bag", "")
                ) for value in contents.split(", ")
            ]
            bag_contents[bag] = contents
            for (amount, container) in contents:
                if "no" != amount:
                    if container in containers_for_bag:
                        if bag not in containers_for_bag[container]:
                            containers_for_bag[container].append(bag)
                    else:
                        containers_for_bag[container] = [bag]

    print("Solution part1: " + str(len(bags_that_can_contain_given_bag("shiny gold", containers_for_bag))))

    timing.log("Part 1 finished!")

    print("Solution part2: " + str(bags_inside_given_bag("shiny gold", bag_contents)))
