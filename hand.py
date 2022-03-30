from typing import List

from card import Card
from deadwood import Deadwood
from melds import Melds


class Hand:
    hands: List[Card] = []
    def __init__(self, cards):
        self.cards = cards
        self.melds = []
        self.deadwood = []
        self.active = False
        __class__.hands.append(self)

    def __repr__(self):
        return self.cards

    def update_hand(self, new_cards: list) -> None:
        """Method to update state of the hand"""
        self.cards = new_cards
        m = Melds(new_cards)
        self.melds = m.melds
        d = Deadwood(new_cards, self.melds)
        self.deadwood = d.get_deadwood()
        self.deadwood.sort(key=lambda x: x.rank)
        self.cards.sort(key=lambda x: x.rank)

    
