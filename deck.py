from card import Card


class Deck:

    """
    Deck Class - creates and instance of a 52 card French deck
    There is no need to access the function directly, unless a user wants to customize
    the Deck Class. Users can specify the number of decks through the CustomizeDeck
    Class.
    """
    id = 0
    def __init__(self, num_decks=1):
        self.deck = []
        id = 0
        for _ in range(num_decks):
            for suit in range(4):
                id += 1
                for rank in range(1, 14):
                    self.deck.append(Card(suit, rank, id))
                    id += 1


class CustomizedDeck:

    """"
    CustomizedDeck Class -

    """
    
    def __init__(self, *_, num_decks=1, remove_suit=None, remove_rank=None, values=None):

        """
        num_decks: integer -- default = 1

        remove_suit: list -- 0 = hearts, 1 = spades, 2 = diamonds, 3 = clubs.
            e.g. remove_suit=[1,2] >> removes all spades and diamonds from the 
            deck

        remove_rank: list -- 1 = ace, 2 = two, 3 = three ... 10 = ten, 11 = jack, 
            12 = queen, 13 = king
            e.g. remove_rank=[2,3,4,5,6] >> removes all two's, three's, four's, 
            five's and six's from the deck

        values: list -- users must specify a list with values for all cards in the 
            deck or leave it at default None - cards that have been removed can be 
            ignored. 
            Example for a full deck: values=[10,2,3,4,5,6,7,8,9,10,10,10,10] 
        """

        deck = Deck(num_decks)
        self.customdeck = deck.deck[:]
        
        self.number_of_suits = 4
        self.number_of_ranks = 13
        if remove_suit:
            if num_decks > 1:
                raise KeyError('not possible to remove cards in multiple decks')
            else:
                self.number_of_suits = self.remove_suits(*remove_suit)  
        if remove_rank:
            if num_decks > 1:
                raise KeyError('not possible to remove cards in multiple decks')
            else:
                self.number_of_ranks = self.remove_ranks(*remove_rank)                  
        if values:
            self.add_values(*values)


    def remove_suits(self, *args):
        to_remove = []
        for card in self.customdeck:
            if card.suit in args:
                to_remove.append(card)
        self.customdeck = list(set(self.customdeck) - set(to_remove))
        return 4 - len(args)


    def remove_ranks(self, *args):
        card_ranks = [card.rank for card in self.customdeck]
        for arg in args:
            if arg in card_ranks:
                for card in self.customdeck:
                    if card.rank in args:
                        self.customdeck.remove(card)
            else:
                raise KeyError('rank not in deck')
        return 13 - len(args)


    def add_values(self, *args):
        j = 0
        for _ in range(self.number_of_suits):
            i = 0
            for _ in range(self.number_of_ranks):
                self.customdeck[j].value = args[i]
                i += 1
                j += 1

    def __getitem__(self, s):
        return self.customdeck[s]

    def __len__(self):
        return len(self.customdeck)

