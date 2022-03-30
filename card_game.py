from copy import deepcopy

import utils
from board import Dealer
from card import Card
from deck import CustomizedDeck
from game_algo import (add_status_to_deadwood_cards, check_gin,
                       choose_card_to_drop, eval_discard, find_discard_card,
                       find_lay_off_cards, human_eval_discard)
from hand import Hand
from player import Player


class CardGame:
    def __init__(self):
        self.deck = CustomizedDeck(values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10])
        self.board = Dealer(self.deck.customdeck, players=2, cards=10)
        self.p1 = Player("Human Player")
        self.p2 = Player("Computer Algo")

    def shuffle_and_deal(self):
        self.board.shuffle_deck()
        self.board.deal_cards()
        self.board.sort_hands()


class GinRummy(CardGame):
    def __init__(self, hands, deck):
        super().__init__()
        self.hands = hands
        self.deck = deck
        self.players = [self.p1, self.p2]
        x = 0
        for hand in self.hands:
            self.players[x].hand = Hand(hand)
            self.players[x].hand.update_hand(hand)
            self.players[x].cards = hand
            x += 1


class GamePlay(GinRummy):
    def __init__(self, hands, deck):
        super().__init__(hands, deck)
        self.discarded_cards = []
        self.rest_of_deck = self.deck[1:]
        self.discard = self.deck[0]
        self.turn = 0
        self.active_player = None
        self.other_player = None
        self.knock = False

    def play_game(self):
        x = 0
        while True:
            self.turn += 1
            self.players[x].active = True
            self.active_player = self.p1 if self.p1.active else self.p2
            self.other_player = self.p1 if self.p2 == self.active_player else self.p2
            self.display_game()
            self.adding_card()
            self.dropping_card()
            if sum([card.value for card in self.active_player.hand.deadwood]) <= 10:
                result = Result(self.active_player, self.other_player)
                self.knock = True
                result.display_result(self.display_game)
                break
            input("\nPress <ENTER> to continue...\n")
            self.players[x].active = False
            x = 1 if x == 0 else 0

    def display_game(self):
        utils.clear_screen()
        print('|-------------------------------Your Hand--------------------------------|')
        print(f'|{utils.display_hand(self.p1).center(72)}|')
        print('|------------------------------------------------------------------------|')
        print('|------------Deadwood------------------------------Melds-----------------|')
        print(f'|  {utils.display_deadwood(self.p1)} [{sum([c.value for c in self.p1.hand.deadwood])}]        {utils.display_melds(self.p1)}     ')
        print('|------------------------------------------------------------------------|')
        print('|                        ----              ----                          |')
        print(f'|                       | {self.discard} |            | XX |                         |')
        print('|                        ----              ----                          |')
        print('|                        [ d]              [ s]                          |')
        print('|                                                                        |')       
        if self.knock:
            print(f'| Lay off: {find_lay_off_cards(self.active_player.hand.melds, self.other_player.hand.deadwood)}                   ')
            print('|------------------------------------------------------------------------|')
            print(f'| melds: {self.p2.hand.melds}  deadwood: {self.p2.hand.deadwood} [{sum([c.value for c in self.p2.hand.deadwood])}]                       ')
        else:
            print('|------------------------------------------------------------------------|')
            print('|                   |XX|XX|XX|XX|XX|XX|XX|XX|XX|XX|XX|                   |')
        print('|------------------------------------------------------------------------|')     
        print('|------------------------------------------------------------------------|')

    def adding_card(self) -> None:
        """Based on evaluation of discarded card, method choses between discarded card and card from the deck"""
        if self.active_player.human:
            add_discard = human_eval_discard()
        else:
            add_discard = eval_discard(
                self.active_player, self.discard, self.discarded_cards
            )

        if add_discard:
            print(f"{self.active_player} adds discard to her hand")
            self.add_card_to_hand(self.discard)
        else:
            card_from_deck = deepcopy(self.rest_of_deck[0])

            if self.active_player.human:
                print(
                    f"{self.active_player} adds {card_from_deck} from the deck to his hand"
                )
            else:
                print(f"{self.active_player} adds a card from the deck to her hand")
            self.add_card_to_hand(self.rest_of_deck[0])

        if self.active_player.human:
            input("Press <ENTER> to continue...")
            self.display_game()

    def add_card_to_hand(self, card: Card) -> None:
        """Method adds chosen card to a hand"""
        self.active_player.cards.append(card)
        self.active_player.hand.update_hand(self.active_player.cards)
        # Round-up of the turn based on card chosen
        if card == self.discard and self.discard in self.discarded_cards:
            self.discarded_cards.remove(self.discard)
        else:
            self.rest_of_deck.pop(0)

    def dropping_card(self):
        """Method evaluates list of cards and choses card to drop from the list"""
        if self.active_player.human:
            dropped_card = choose_card_to_drop(self.p1)
        else:
            add_status_to_deadwood_cards(
                self.active_player.hand.deadwood, self.discarded_cards, self.turn
            )
            dropped_card = find_discard_card(
                self.discard, self.active_player
            )
        self.discard = dropped_card
        self.active_player.cards.remove(dropped_card)
        self.active_player.hand.update_hand(self.active_player.cards)
        self.discarded_cards.append(dropped_card)


class Result:
    def __init__(self, active_player, other_player):
        self.active_player = active_player
        self.other_player = other_player

    def display_result(self, display):
        """Method prints the result of a round"""
        display()
        print("\nWE HAVE A WINNER!!!")
        active_deadwood_sum = sum(
            [card.value for card in self.active_player.hand.deadwood]
        )
        other_deadwood_sum = sum(
            [card.value for card in self.other_player.hand.deadwood]
        )
        winner = (
            self.active_player
            if active_deadwood_sum < other_deadwood_sum
            else self.other_player
        )
        points = (
            other_deadwood_sum - active_deadwood_sum
            if winner == self.active_player
            else active_deadwood_sum - other_deadwood_sum
        )
        if check_gin(self.active_player.hand.deadwood):
            print("! ! !  G I N  ! ! !")
            points += 25
        print(f"Winner is {str(winner).upper()}")
        print(f"{winner} scored {points} points")
        input("Press <ENTER> to continue.")
