from tools import timing

class Cup:

    def __init__(self, cup, prev_cup, next_cup):
        self.cup = cup
        self.prev_cup = prev_cup,
        self.next_cup = next_cup


def create_linked_list_and_map(cup_circle):
    first_cup = None
    last_cup = None
    cup_map = {}
    for i in range(len(cup_circle)):
        if not first_cup:
            cup = Cup(cup_circle[i], None, None)
            first_cup = cup
        else:
            cup = Cup(cup_circle[i], last_cup, None)
            last_cup.next_cup = cup
        cup_map[cup.cup] = cup
        last_cup = cup
    first_cup.prev_cup = last_cup
    last_cup.next_cup = first_cup
    return first_cup, cup_map


def run_cup_round(current_cup, cup_map):
    moved_cup_1 = current_cup.next_cup
    moved_cup_2 = moved_cup_1.next_cup
    moved_cup_3 = moved_cup_2.next_cup
    moved_cups = {moved_cup_1.cup, moved_cup_2.cup, moved_cup_3.cup}
    moved_cup_3.next_cup.prev_cup = current_cup
    current_cup.next_cup = moved_cup_3.next_cup

    cup_before_moved_cups = (((current_cup.cup - 2) + len(cup_map)) % len(cup_map)) + 1
    while cup_before_moved_cups in moved_cups:
        cup_before_moved_cups = (((cup_before_moved_cups - 2) + len(cup_map)) % len(cup_map)) + 1
    cup_before_moved_cups = cup_map[cup_before_moved_cups]
    cup_before_moved_cups.next_cup.prev_cup = moved_cup_3
    moved_cup_3.next_cup = cup_before_moved_cups.next_cup
    cup_before_moved_cups.next_cup = moved_cup_1
    moved_cup_1.prev_cup = cup_before_moved_cups
    return current_cup.next_cup




def cup_round(cup_circle, index_current_cup, current_cup):
    new_cup_circle = []
    moved_cups = [
        cup_circle[(index_current_cup + 1) % len(cup_circle)],
        cup_circle[(index_current_cup + 2) % len(cup_circle)],
        cup_circle[(index_current_cup + 3) % len(cup_circle)]
    ]
    cup_before_moved_cups = (((current_cup - 2) + len(cup_circle)) % len(cup_circle)) + 1
    while cup_before_moved_cups in moved_cups:
        cup_before_moved_cups = (((cup_before_moved_cups - 2) + len(cup_circle)) % len(cup_circle)) + 1
    for cup in cup_circle:
        if cup == current_cup:
            index_current_cup = len(new_cup_circle)
        if cup not in moved_cups:
            new_cup_circle.append(cup)
        if cup == cup_before_moved_cups:
            new_cup_circle.extend(moved_cups)

    cup_circle = new_cup_circle
    index_current_cup = (index_current_cup + 1) % len(cup_circle)
    current_cup = cup_circle[index_current_cup]
    return cup_circle, index_current_cup, current_cup,


def day23():
    cup_circle = [4, 8, 7, 9, 1, 2, 3, 6, 5]
    index_current_cup = 0
    current_cup = cup_circle[index_current_cup]
    for _ in range(100):
        (cup_circle, index_current_cup, current_cup) = cup_round(cup_circle, index_current_cup, current_cup)

    index_cup_1 = cup_circle.index(1)
    solution_part_1 = ""
    for i in range(1, len(cup_circle)):
        solution_part_1 += str(cup_circle[(index_cup_1 + i) % len(cup_circle)])

    print("Solution part1:", solution_part_1)

    timing.log("Part 1 finished!")

    cup_circle = [4, 8, 7, 9, 1, 2, 3, 6, 5]
    cup_circle.extend(range(len(cup_circle) + 1, 1000001))
    (current_cup, cup_map) = create_linked_list_and_map(cup_circle)
    for _ in range(10000000):
        current_cup = run_cup_round(current_cup, cup_map)

    solution_part_2 = cup_map[1].next_cup.cup * cup_map[1].next_cup.next_cup.cup

    print("Solution part2:", solution_part_2)
