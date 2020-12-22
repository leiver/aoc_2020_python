from tools import timing
import os
import sys


def intersection(lst1, lst2):
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3


def day21():
    all_ingredients = []
    ingredients_could_contain_allergen = {}
    ingredient_count = {}
    with open(os.path.join(sys.path[0], "inputs/input_day21.txt"), "r") as file:
        for line in file:
            (ingredients, allergens) = line.rstrip().strip(")").split(" (contains ")
            ingredients = ingredients.split(" ")
            all_ingredients = list(set(ingredients) | set(all_ingredients))
            allergens = allergens.split(", ")
            for ingredient in ingredients:
                if ingredient in ingredient_count:
                    ingredient_count[ingredient] = ingredient_count[ingredient] + 1
                else:
                    ingredient_count[ingredient] = 1
            for allergen in allergens:
                if allergen not in ingredients_could_contain_allergen:
                    ingredients_could_contain_allergen[allergen] = ingredients
                else:
                    ingredients_could_contain_allergen[allergen] = intersection(ingredients_could_contain_allergen[allergen], ingredients)

    ingredients_with_no_allergen = all_ingredients.copy()
    for ingredients_with_possible_allergen in ingredients_could_contain_allergen.values():
        ingredients_with_no_allergen = [ingredient for ingredient in ingredients_with_no_allergen if ingredient not in ingredients_with_possible_allergen]

    solution_part1 = 0
    for ingredient_with_no_allergen in ingredients_with_no_allergen:
        solution_part1 += ingredient_count[ingredient_with_no_allergen]

    print("Solution part1:", solution_part1)

    ingredients_with_known_allergen = {}
    allergens_with_known_ingredient = {}
    while len(ingredients_with_known_allergen) != len(ingredients_could_contain_allergen):
        for (allergen, ingredients) in ingredients_could_contain_allergen.items():
            filtered_ingredients = [ingredient for ingredient in ingredients if ingredient not in ingredients_with_known_allergen.keys()]
            if len(filtered_ingredients) == 1:
                ingredients_with_known_allergen[filtered_ingredients[0]] = allergen
                allergens_with_known_ingredient[allergen] = filtered_ingredients[0]


    allergens_with_known_ingredient_list = list(allergens_with_known_ingredient.keys())
    allergens_with_known_ingredient_list.sort()
    print("Solution part2:", ",".join([allergens_with_known_ingredient[allergen] for allergen in allergens_with_known_ingredient_list]))
