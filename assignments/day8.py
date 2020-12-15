from tools import timing
import os
import sys


def find_loop_or_end(instructions_to_parse):
    loop_of_instructions = []
    parsed_instructions = {}
    # define loop
    accumulator = 0
    pointer = 0
    while pointer < len(instructions_to_parse):
        if pointer in parsed_instructions or pointer == len(instructions_to_parse):
            return accumulator, loop_of_instructions
        (command_to_parse, number_to_parse) = instructions_to_parse[pointer]
        parsed_instructions[pointer] = 1
        loop_of_instructions.append((pointer, (command_to_parse, number_to_parse)))
        if command_to_parse == "acc":
            accumulator += int(number_to_parse)
            pointer += 1
        elif command_to_parse == "jmp":
            pointer += int(number_to_parse)
        elif command_to_parse == "nop":
            pointer += 1

    return accumulator, []


def day8():
    instructions = []
    with open(os.path.join(sys.path[0], "inputs/input_day8.txt"), "r") as file:
        for line in file:
            (command, number) = line.split(" ")
            instructions.append((command, number))

    (solution_part1, initial_loop_of_instructions) = find_loop_or_end(instructions)

    print("Solution part1: " + str(solution_part1))

    timing.log("Part 1 finished!")

    for (changed_instruction, (command, number)) in initial_loop_of_instructions:
        if command in ["jmp", "nop"]:
            if command == "jmp":
                instructions[changed_instruction] = ("nop", instructions[changed_instruction][1])
            else:
                instructions[changed_instruction] = ("jmp", instructions[changed_instruction][1])

            (acc, loop_if_any) = find_loop_or_end(instructions)

            if not loop_if_any:
                print("Solution part2: " + str(acc))
                break

            instructions[changed_instruction] = (command, instructions[changed_instruction][1])
