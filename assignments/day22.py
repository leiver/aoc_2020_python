from tools import timing
import os
import sys
from collections import deque


def calculate_score(deck):
    deck = list(deck)
    result = 0
    for i in range(1, len(deck) + 1):
        result += deck[i * -1] * i
    return result


def play_recursive_game(player_1_deck, player_2_deck):
    if len(player_1_deck) == 0:
        return 2, player_2_deck
    elif len(player_2_deck) == 0:
        return 1, player_1_deck
    deck_states_player_1 = set()
    deck_states_player_2 = set()
    while len(player_1_deck) > 0 and len(player_2_deck) > 0:
        player_1_frozen = frozenset(player_1_deck)
        player_2_frozen = frozenset(player_2_deck)
        if player_1_frozen in deck_states_player_1 or player_2_frozen in deck_states_player_2:
            return 1, player_1_deck
        deck_states_player_1.add(player_1_frozen)
        deck_states_player_2.add(player_2_frozen)

        card_player_1 = player_1_deck.popleft()
        card_player_2 = player_2_deck.popleft()

        if card_player_1 <= len(player_1_deck) and card_player_2 <= len(player_2_deck):
            (winning_player, _) = play_recursive_game(deque(list(player_1_deck)[:card_player_1]), deque(list(player_2_deck)[:card_player_2]))
        elif card_player_1 > card_player_2:
            winning_player = 1
        else:
            winning_player = 2

        if winning_player == 1:
            player_1_deck.append(card_player_1)
            player_1_deck.append(card_player_2)
            winning_deck = player_1_deck
        else:
            player_2_deck.append(card_player_2)
            player_2_deck.append(card_player_1)
            winning_deck = player_2_deck

    return winning_player, winning_deck


def play_regular_game(player_1_deck, player_2_deck):
    while len(player_1_deck) > 0 and len(player_2_deck) > 0:
        card_player_1 = player_1_deck.popleft()
        card_player_2 = player_2_deck.popleft()

        if card_player_1 > card_player_2:
            winning_deck = player_1_deck
            winning_deck.append(card_player_1)
            winning_deck.append(card_player_2)
        else:
            winning_deck = player_2_deck
            winning_deck.append(card_player_2)
            winning_deck.append(card_player_1)
    return winning_deck


def day22():
    with open(os.path.join(sys.path[0], "inputs/input_day22.txt"), "r") as file:
        (initial_deck_player_1, initial_deck_player_2) = file.read().rstrip().split("\n\n")
        initial_deck_player_1 = deque([int(card) for card in initial_deck_player_1.rstrip().split("\n")[1:]])
        initial_deck_player_2 = deque([int(card) for card in initial_deck_player_2.rstrip().split("\n")[1:]])

    print("Solution part1:", calculate_score(play_regular_game(initial_deck_player_1.copy(), initial_deck_player_2.copy())))

    timing.log("Part 1 finished!")

    print("Solution part2:", calculate_score(play_recursive_game(initial_deck_player_1.copy(), initial_deck_player_2.copy())[1]))
