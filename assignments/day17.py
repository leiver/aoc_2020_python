from tools import timing
import os
import sys


def day16():
    dimension_map = {}

    with open(os.path.join(sys.path[0], "inputs/input_day17.txt"), "r") as file:
        
