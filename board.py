import random

from deck import CustomizedDeck


class Dealer:

    """Dealer Class - Once the deck is created the dealer is brought in and picks it up."""

    def __init__(self, deck: CustomizedDeck, players: int, cards: int):
        self.players = players
        self.cards = cards
        self.playdeck = deck[:]


    def shuffle_deck(self):
        random.shuffle(self.playdeck)


    def set_trump(self, suit):
        suits = {card.suit for card in self.playdeck}
        if len(suits) == 4:
            for card in self.playdeck:
                if card.suit == suit:
                    card.trump = True
                else:
                    card.trump = False
            suit_name = ('hearts' if suit == 0 else 'spades' if suit == 1 else 'diamonds' 
            if suit == 2 else 'clubs')
            return suit_name
        raise KeyError('trump suit can only be set in decks with 4 suits')


    def deal_cards(self):
        self.hands = []
        for _ in range(self.players):
            self.hands.append(list())
        for _ in range(self.cards):
            for hand in range(len(self.hands)):    
                self.hands[hand].append(self.playdeck[0])
                self.playdeck.pop(0)


    def sort_hands(self):
        for hand in self.hands:
            hand.sort(key=lambda x: x.rank)


    def compare_hands_value(self, hand1, hand2):
        if hand1[0].value is not None:
            total_value1 = sum([card.value for card in hand1])
            total_value2 = sum([card.value for card in hand2])
        else:
            total_value1 = sum([card.rank for card in hand1])
            total_value2 = sum([card.rank for card in hand2])
        if total_value1 - total_value2 > 0:
            return hand1
        return hand2


    def compare_cards(self, seq):
        trump_seq = [card for card in self.playdeck if card.trump == True]
        if seq[0].value is not None:
            if trump_seq:               
                return max(trump_seq, key=lambda x: x.value)
            else:
                max_card = seq[0]               
                for card in seq:
                    if card.value > max_card.value:
                        max_card = card                       
                return max_card
        else:
            if trump_seq:
                trump_seq = [card for card in self.playdeck if card.trump == True]
                return max(trump_seq, key=lambda x: x.rank)
            else:
                return max(seq)



