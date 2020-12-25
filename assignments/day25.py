from tools import timing
import os
import sys
from collections import deque


def day25():
    subject_number = 7
    card_public_key = 9717666
    door_public_key = 20089533

    result = 1
    loop_count = 0
    while result != card_public_key:
        result *= subject_number
        result = result % 20201227
        loop_count += 1
    print(loop_count)

    subject_number = door_public_key
    encryption_key = 1
    for _ in range(loop_count):
        encryption_key *= subject_number
        encryption_key = encryption_key % 20201227

    print("Solution part1:", encryption_key)
