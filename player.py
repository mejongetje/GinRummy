class Player:
    """Class creates a Player"""
    def __init__(self, name, human=False):
        self.name = name
        self.active = False
        self.hand = None
        self.cards = []
        self.human = human
   
    @property
    def deadwood(self):
        return self.hand.deadwood

    @property
    def melds(self):
        return self.hand.melds

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name
