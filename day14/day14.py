from tools import timing
import os
import sys


def write_to_address(index_binary, mask_binary, index, mem, value):
    if index == len(index_binary):
        mem["value"] = value
    elif mask_binary[index] == "X":
        mem_1 = {}
        if "1" in mem:
            mem_1 = mem["1"]
        else:
            mem["1"] = mem_1
        write_to_address(index_binary, mask_binary, index+1, mem_1, value)
        mem_0 = {}
        if "0" in mem:
            mem_0 = mem["0"]
        else:
            mem["0"] = mem_0
        write_to_address(index_binary, mask_binary, index+1, mem_0, value)
    else:
        mem_bit = index_binary[index]
        if mask_binary[index] == "1":
            mem_bit = "1"
        mem_to_write = {}
        if mem_bit in mem:
            mem_to_write = mem[mem_bit]
        else:
            mem[mem_bit] = mem_to_write
        write_to_address(index_binary, mask_binary, index+1, mem_to_write, value)


def get_all_values_from_memory(memory):
    value = 0
    if "value" in memory:
        value += memory["value"]
    if "0" in memory:
        value += get_all_values_from_memory(memory["0"])
    if "1" in memory:
        value += get_all_values_from_memory(memory["1"])
    return value


def day14():
    memory = {}
    memory_part_2 = {}
    mask = ""
    with open(os.path.join(sys.path[0], "day14/input_day14.txt"), "r") as file:
        for line in file:
            (command, value) = line.rstrip().split(" = ")
            if command == "mask":
                mask = value
            elif "mem" in command:
                mem_index = int(command[command.index("[")+1:command.index("]")])
                mem_index_binary = '{0:036b}'.format(mem_index)
                mem_value = '{0:036b}'.format(int(value))

                fixed_mem_value = ""
                for mem_value_index in range(len(mem_value)):
                    if mask[mem_value_index] != "X":
                        fixed_mem_value += mask[mem_value_index]
                    else:
                        fixed_mem_value += mem_value[mem_value_index]
                memory[mem_index] = fixed_mem_value

                write_to_address(mem_index_binary, mask, 0, memory_part_2, int(value))

    solution_part_1 = 0
    for value in memory.values():
        solution_part_1 += int(value, base=2)

    print("Solution part1: ", solution_part_1)

    timing.log("Part 1 finished!")

    solution_part_2 = get_all_values_from_memory(memory_part_2)

    print("Solution part2: ", solution_part_2)