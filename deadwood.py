from itertools import chain


class Deadwood:

    def __init__(self, cards, melds):
        self.cards = cards
        self.melds = melds
        self.discarded_cards = []
        self.deadwood = self.get_deadwood()

    def get_deadwood(self) -> list:
        """Method returns list of cards by deducting cards in runs and sets from list of cards"""
        deadwood = []
        for card in self.cards:
            if card not in list(chain(*self.melds)):
                deadwood.append(card)
        return deadwood



    