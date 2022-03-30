from os import name, system


def clear_screen():
    if name == "nt":
        system("cls")
    else:
        system("clear")


def display_hand(player):
    i = 1
    strng = ' '
    for card in player.hand.cards:
        strng += '['+str(i)+']'+ card.name + '  '
        i += 1
    return strng


def display_melds(player):
    strng = ' '
    for meld in player.hand.melds:
        strng += str(meld) + ' '
    return strng


def display_deadwood(player):
    return str(player.hand.deadwood)
