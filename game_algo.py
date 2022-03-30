from copy import deepcopy
from functools import reduce
from itertools import chain, groupby, takewhile
from typing import Generator, List

import more_itertools as mit

from card import Card
from melds import find_runs, find_sets
from player import Player


# Helper functions to choose between two cards, the open and the closed card
def human_eval_discard() -> bool:
    """Function asks human player if she wants to add discard to her hand"""
    print("It's your turn!")
    choice = input("Type [d] if you want the open card, [s] for a card from the deck:  ")
    if choice == "d":
        return True
    return False

def eval_discard(player: Player, discard: Card, discarded_cards) -> bool:
    """Function decides if a specific card should be added to a sequence of cards"""
    deadwood_copy = deepcopy(player.hand.deadwood)
    high_card_value = max([card.value for card in deadwood_copy])
    high_card = [card for card in deadwood_copy if card.value == high_card_value]
    deadwood_copy.append(discard)
    new_runs_it = find_runs(deadwood_copy)
    new_runs = list(new_runs_it)
    new_sets = find_sets(deadwood_copy)
    if new_runs or new_sets:
        return True
    deadwood_copy.remove(high_card[0])
    if sum([card.value for card in deadwood_copy]) <= 10:
        return True
    deadwood_copy.append(high_card[0])
    triangle_check = check_for_triangles(discard, deadwood_copy, discarded_cards)
    if triangle_check == 4:
        return True
    for meld in player.melds:
        if discard.rank == meld[0].rank and discard.rank == meld[1].rank:
            return True
        if (discard.id + 1) == list(meld)[0].id or (discard.id - 1) == list(meld)[-1].id:
            if discard.suit == meld[0].suit:
                return True
    return False


# Functions for adding a status to a card in a list: "the deadwood"
def add_status_to_deadwood_cards(deadwood: list, discarded_cards: list, turn: int) -> None:
    """Cards in sequence of cards are given a status value"""
    for card in deadwood:
        if card.value <= 6:
            card.status = 0
        else:
            card.status = -1
        open_couple = check_for_open_couples(card, deadwood, discarded_cards)
        if open_couple:
            card.status = open_couple
        pair = check_for_pairs(card, deadwood, discarded_cards)
        if pair:
            card.status = pair
        couple = check_for_couples(card, deadwood, discarded_cards)
        if couple:
            card.status = couple
        triangle = check_for_triangles(card, deadwood, discarded_cards)
        if triangle:
            card.status = triangle
        if turn > 6 and card.value >= 6:
            card.status -= 2


def check_for_triangles(card: Card, deadwood: list, discarded_cards: list) -> int:
    """Function checks if a card in a list of cards is a member of a triangle, e.g. [3h,3c,2c]"""
    status_value = 0
    deadwood_copy = deepcopy(deadwood)
    deadwood_ids = [c.id for c in deadwood_copy]
    if len([c for c in deadwood_copy if c.rank == card.rank]) == 2 and card.rank != 13:
        if card.id +1 in deadwood_ids:
            status_value = check_triangle_missing_cards_1(card, discarded_cards)
            return status_value
        if card.id -1 in deadwood_ids:
            status_value = check_triangle_missing_cards_1(card, discarded_cards, id_plus=False)
            return status_value
    pairs = search_pairs_in_deadwood(deadwood)
    if pairs:
        pairs_id = [pair_card.id for pair_card in chain(*pairs) if pair_card.rank != 13]
        if card.id +1 in pairs_id and card.rank != 13:
            status_value = check_triangle_missing_cards_2(card, discarded_cards)
            return status_value
        if card.id -1 in pairs_id and card.rank != 13:
            status_value = check_triangle_missing_cards_2(card, discarded_cards, id_plus=False)
            return status_value
    couples_it = search_couples_in_deadwood(deadwood)
    couples = list(couples_it)
    if couples:
        couples_rank = [couple_card.rank for couple_card in chain(*couples) if couple_card.id != card.id]
        if card.rank in couples_rank and card.rank != 13:
            status_value = check_triangle_missing_cards_3(card, discarded_cards, couples)
            return status_value
    return status_value


def check_triangle_missing_cards_1(card: Card, discarded_cards: list, id_plus=True) -> int:
    """Helper function to add status to card in sequence of cards"""
    status_value = 4
    disc_ids = [c.id for c in discarded_cards]
    card_id = card.id+1 if id_plus else card.id-1
    same_rank = [c for c in discarded_cards if c.rank == card.rank and c.id != card.id and c.id != card_id]
    status_value = status_value - len(set(same_rank)) if same_rank else status_value
    status_value = status_value - 1 if (card.id+2 in disc_ids and id_plus) or \
        (card.id-2 in disc_ids and not id_plus) else status_value
    status_value = status_value - 1 if (card.id-1 in disc_ids and id_plus) or \
        (card.id+1 in disc_ids and not id_plus) else status_value
    return status_value


def check_triangle_missing_cards_2(card, discarded_cards, id_plus=True):
    """Helper function to add status to card in sequence of cards"""
    status_value = 4
    disc_ids = [c.id for c in discarded_cards]
    status_value = status_value - 1 if (card.id+2 in disc_ids and id_plus) or \
        (card.id-2 in disc_ids and not id_plus) else status_value
    status_value = status_value - 1 if (card.id-1 in disc_ids and id_plus) or \
        (card.id+1 in disc_ids and not id_plus) else status_value
    return status_value


def check_triangle_missing_cards_3(card, discarded_cards, couples):
    """Helper function to add status to card in sequence of cards"""
    status_value = 4
    if card.rank in [c.rank for c in discarded_cards if c.id != card.id]:
        status_value -= 1
    for couple in couples:
        couple.sort(key=lambda x: x.id)
        if couple[0].id -1 in [c.id for c in discarded_cards]:
            status_value -= 1
        if couple[1].id +1 in [c.id for c in discarded_cards]:
            status_value -= 1
    return status_value


def search_pairs_in_deadwood(deadwood) -> list:
    """Function returns a list of pairs in a sequence of cards, e.g. [2h, 2c]"""
    hand_copy = deepcopy(deadwood)
    hand_sort = sorted(hand_copy, key=lambda x: x.rank)
    pairs = []        
    result = groupby(hand_sort, key=lambda x: x.rank)
    groups_list = [(key, list(items)) for key, items in result]
    for i in range(len(groups_list)):
        pair = groups_list[i][1]
        if len(pair) == 2:
            pairs += [pair]
    return pairs


def search_couples_in_deadwood(deadwood) -> Generator:
    """Function returns all couples in a sequence of cards, eg [3h, 2h]"""
    hand_copy = deepcopy(deadwood)
    hand_id = [card.id for card in hand_copy]
    hand_id.sort()
    for group in mit.consecutive_groups(hand_id):
        group = list(group)
        if len(group) == 2:
            couples = [card for card in hand_copy for id in group if id == card.id]
            couples.sort()
            yield couples
        else:
            pass


def check_for_pairs(card: Card, deadwood: list, discarded_cards: list) -> int:
    """Function checks if there are pairs in a sequence of cards, e.g. [2h,2c]"""
    deadwood_copy = deepcopy(deadwood)
    status_value = 0
    if card.rank in [c.rank for c in deadwood_copy if c.id != card.id]:
        status_value += 2
        card_ranks = [c for c in discarded_cards if c.id != card.id and c.rank == card.rank]
        if card in card_ranks:
            status_value -= 1
    return status_value


def check_for_couples(card: Card, deadwood: list, discarded_cards: list) -> int:
    """Function checks if there are couples in a sequence of cards, e.g. [2h, 3h]"""
    status_value = 0
    deadwood_copy = deepcopy(deadwood)
    deadwood_ids = [c.id for c in deadwood_copy]
    if card.id +1 in deadwood_ids:
        status_value += 2
        if card.id +2 in [c.id for c in discarded_cards]:
            status_value -= 1
        if card.id -1 in [c.id for c in discarded_cards]:
            status_value -= 1
    elif card.id -1 in deadwood_ids:
        status_value += 2
        if card.id -2 in [c.id for c in discarded_cards]:
            status_value -= 1
        if card.id +1 in [c.id for c in discarded_cards]:
            status_value -= 1
    return status_value


def check_for_open_couples(card: Card, deadwood: list, discarded_cards: list) -> int:
    """Function checks if there are open couples in a sequence of cards, e.g. [2h, 4h]"""
    deadwood_copy = deepcopy(deadwood)
    status_value = 0
    if card.id +2 in [c.id for c in deadwood_copy if c.suit == card.suit]:
        status_value += 1
        if card.id + 1 in [c.id for c in discarded_cards]:
            status_value -= 2
    elif card.id -2 in [c.id for c in deadwood_copy if c.suit == card.suit]:
        status_value += 1
        if card.id - 1 in [c.id for c in discarded_cards]:
            status_value -= 2
    return status_value


# Functions that help to choose a card to drop from a list: "the deadwood"

def choose_card_to_drop(player):
    """Function asks human player which card she wants to drop"""
    print("It's your turn!")
    card_to_drop = int(input("Which card do you want to discard? "))
    return player.hand.cards[card_to_drop-1]


def find_discard_card(current_discard: Card, active_player: Player) -> Card:
    """Function evaluates which card to remove from a sequence of cards"""
    card_status = []
    for card in active_player.hand.deadwood:
        if card.id != current_discard.id:
            card_status.append(card)
    card_status.sort(key=lambda x: x.status)
    int_val = takewhile(lambda x: x.status==card_status[0].status, card_status)
    int_val2 = list(sorted(int_val, key=lambda x: x.value))
    if int_val2:
        discard_card = int_val2[-1]
    else:
        discard_meld = reduce(lambda a, b: a if len(a) > len(b) and a[0].rank != a[1].rank else b, active_player.hand.melds)
        discard_card = discard_meld[0]
    return discard_card


# Functions that help to find the winner of the game

def find_lay_off_cards(active_melds, other_deadwood) -> List[Card]:
    """Function checks if cards in a sequence of deadwood cards can be added to one of the opponents melds"""
    lay_off: list = []
    lay_off_couples: list = []
    couples_it = search_couples_in_deadwood(other_deadwood)
    couples = list(couples_it)
    for couple in couples:
        for card in couple:
            for meld in active_melds:
                if meld[0].suit == card.suit and meld[1].id == card.id + 2:
                    lay_off_couples.append(couple)
                elif meld[-1].suit == card.suit and meld[-2].id == card.id - 2:
                    lay_off_couples.append(couple)
    for card in set(other_deadwood) - set(chain(*lay_off_couples)):
        for meld in active_melds:
            if meld[0].rank == card.rank and meld[1].rank == card.rank:
                lay_off.append(card)
            elif meld[0].suit == card.suit and meld[1].id == card.id + 2:
                lay_off.append(card)
            elif meld[-1].suit == card.suit and meld[-2].id == card.id - 2:
                lay_off.append(card)
    lay_off_cards = set(lay_off) | set(chain(*lay_off_couples))
    for card in lay_off_cards:
        other_deadwood.remove(card)
    return list(lay_off_cards)

def check_gin(active_deadwood):
    if sum([card.value for card in active_deadwood]) == 0:
        return True
    return False
