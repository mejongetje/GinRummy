from card_game import CardGame, GamePlay, GinRummy


def main():
    game = CardGame()
    game.shuffle_and_deal()
    gin_rummy = GinRummy(game.board.hands)
    play = GamePlay(gin_rummy.hands)
    play.play_game()


if __name__ == "__main__":
    main()
