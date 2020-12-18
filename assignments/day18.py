from tools import timing
import os
import sys


def evaluate_expression(expression):
    sum_of_expression = 0
    index = 0
    parentheses = 0
    parentheses_index = 0
    operand = "."
    for element in expression:
        if parentheses > 0:
            if element == "(":
                parentheses += 1
            elif element == ")":
                parentheses -= 1
                if parentheses == 0:
                    number = evaluate_expression(expression[parentheses_index+1:index])
                    if operand == "+":
                        sum_of_expression += number
                    elif operand == "*":
                        sum_of_expression *= number
                    else:
                        sum_of_expression = number
        else:
            if element == "(":
                parentheses += 1
                parentheses_index = index
            elif element == "+" or element == "*":
                operand = element
            elif element.isnumeric():
                number = int(element)
                if operand == "+":
                    sum_of_expression += number
                elif operand == "*":
                    sum_of_expression *= number
                else:
                    sum_of_expression = number
        index += 1
    return sum_of_expression


def evaluate_expression_part_2(expression):
    sum_of_expression = 0
    index = 0
    parentheses = 0
    parentheses_index = 0
    operand = "."
    sum_after_multiply = -1
    for element in expression:
        if parentheses > 0:
            if element == "(":
                parentheses += 1
            elif element == ")":
                parentheses -= 1
                if parentheses == 0:
                    number = evaluate_expression_part_2(expression[parentheses_index+1:index])
                    if operand == "+":
                        if sum_after_multiply != -1:
                            sum_after_multiply += number
                        else:
                            sum_of_expression += number
                    elif operand == "*":
                        if sum_after_multiply != -1:
                            sum_of_expression *= sum_after_multiply
                            sum_after_multiply = number
                        else:
                            sum_after_multiply = number
                    else:
                        sum_of_expression = number
        else:
            if element == "(":
                parentheses += 1
                parentheses_index = index
            elif element == "+" or element == "*":
                operand = element
            elif element.isnumeric():
                number = int(element)
                if operand == "+":
                    if sum_after_multiply != -1:
                        sum_after_multiply += number
                    else:
                        sum_of_expression += number
                elif operand == "*":
                    if sum_after_multiply != -1:
                        sum_of_expression *= sum_after_multiply
                        sum_after_multiply = number
                    else:
                        sum_after_multiply = number
                else:
                    sum_of_expression = number
        index += 1
    if sum_after_multiply != -1:
        sum_of_expression *= sum_after_multiply
    return sum_of_expression


def day18():

    sum_of_sums = 0
    sum_part_2 = 0
    with open(os.path.join(sys.path[0], "inputs/input_day18.txt"), "r") as file:
        for expression in file:
            sum_of_sums += evaluate_expression(expression.rstrip())
            sum_part_2 += evaluate_expression_part_2(expression.rstrip())

    print("Solution part1: ", sum_of_sums)

    print("Solution part2: ", sum_part_2)
