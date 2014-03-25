'''
Python 2.7

This module contains the main program logic.
'''
import strategies
import game
import user_input

def main():
    strategies.human.__name__ = "Human"
    strategies.perfect.__name__ = "Computer"


    print "Let's play tic-tac-toe!\n"
    again = "y"
    while again == "y":
        go_first = user_input.get_input("Would you like to go first (y or n)?", ("y", "n"))
        print "\n"
        if go_first == "y":
            first = strategies.human
            second = strategies.perfect
        else:
            first = strategies.perfect
            second = strategies.human
        g = game.Game(first, second)
        g.play_game(display=True)
        again = user_input.get_input("Would you like to play again (y or n)?", ("y", "n"))


if __name__ == "__main__":
    main()
