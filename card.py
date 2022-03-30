class Card:

    """
    Card Class - creates a card instance with a specified suit and rank. 
    The suit and rank are matched with the list provided in the class to get the 
    cards name.

    Card instances can be compared with eachother, through the __lt__ method.
    The __eq__ method is not used, to avoid conflicts with hashing, which is 
    used in the CustomizeDeck class. Equalitity can be tested with card.rank
    or card.value.
    """
    card_suit = ["\u2665", "\u2666", "\u2660", "\u2663"]
    card_rank = list('A23456789TJQK')

    def __init__(self, suit: int, rank: int, id: int):
        self.suit = suit
        self.rank = rank
        self.id = id
        self.value = None
        self.status = None
        self.trump = False
        
        self.name = f'{Card.card_rank[self.rank-1]}{Card.card_suit[self.suit]}'


    def __repr__(self):
        return self.name


    # def __iter__(self):
    #     return self


    def __lt__(self, other):
        if self.trump and other.trump:
            if self.value:
                return self.value < other.value
            else:
                return self.rank < other.rank
        elif self.trump and other.trump is False:
            return self.rank < 0
        elif other.trump and self.trump is False:
            return self.rank < 100
        elif self.value:
            return self.value < other.value
        else:
            return self.rank < other.rank


    def __add__(self, other):
        if isinstance(other, Card):
            if self.value:
                return self.value + other.value
            else:
                return self.rank + other.rank

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.name)


