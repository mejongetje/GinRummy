from card_game import CardGame, GamePlay, GinRummy


def main():
    game = CardGame()
    game.shuffle_and_deal()
    gin_rummy = GinRummy(game.board.hands, game.board.playdeck)
    play = GamePlay(gin_rummy.hands, gin_rummy.deck)
    play.play_game()


if __name__ == "__main__":
    main()
