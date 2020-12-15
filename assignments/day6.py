from tools import timing
import os
import sys


def intersection(lst1, lst2):
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3


def day6():
    total_questions_any_answered = total_questions_all_answered = 0
    with open(os.path.join(sys.path[0], "inputs/input_day6.txt"), "r") as file:
        for group in file.read().split("\n\n"):
            any_answered_questions = []
            all_answered_questions = []
            for person in group.rstrip().split("\n"):
                answers_from_person = [char for char in person]
                if not any_answered_questions:
                    all_answered_questions = answers_from_person
                elif all_answered_questions:
                    all_answered_questions = intersection(all_answered_questions, answers_from_person)
                any_answered_questions = list(set(any_answered_questions) | set(answers_from_person))
            total_questions_any_answered += len(any_answered_questions)
            total_questions_all_answered += len(all_answered_questions)

    print("Solution part1: " + str(total_questions_any_answered))
    print("Solution part2: " + str(total_questions_all_answered))
