import timing
import os
import sys


def find_loop_or_end(instructions_to_parse):
    loop_of_instructions = []
    parsed_instructions = {}
    # define loop
    acc = 0
    pointer = 0
    while pointer < len(instructions_to_parse):
        if pointer in parsed_instructions or pointer == len(instructions_to_parse):
            return acc, loop_of_instructions
        (command, number) = instructions_to_parse[pointer]
        parsed_instructions[pointer] = 1
        loop_of_instructions.append((pointer, (command, number)))
        if command == "acc":
            acc += int(number)
            pointer += 1
        elif command == "jmp":
            pointer += int(number)
        elif command == "nop":
            pointer += 1

    return acc, []


instructions = []
with open(os.path.join(sys.path[0], "input_day8.txt"), "r") as file:
    for line in file:
        (command, number) = line.split(" ")
        instructions.append((command, number))

(solution_part1, initial_loop_of_instructions) = find_loop_or_end(instructions)

print("Solution part1: " + str(solution_part1))
timing.log("Part 1 finished")

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
