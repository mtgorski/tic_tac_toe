'''
Python 2.7

This module contains the main program logic.
'''
import strategies
import game


def get_input(prompt, options=None):
    '''
    Asks the user for input, using the prompt. If options are specified,
    repeats the question until the answer is in the options.

    *Arguments
    prompt (str): the phrase displayed to the user when asking for input
    options (collection): container of valid inputs as strings
    
    '''
    while True:
        answer = raw_input(prompt+"  ")
        if options and answer not in options:
            print "That's not a valid input."
            print "Valid options are: "+", ".join(options)+".\n"
        else:
            break
    return answer


def main():
    strategies.human.__name__ = "Human"
    strategies.perfect.__name__ = "Computer"


    print "Let's play tic-tac-toe!\n"
    again = "y"
    while again == "y":
        go_first = get_input("Would you like to go first (y or n)?", ("y", "n"))
        print "\n"
        if go_first == "y":
            first = strategies.human
            second = strategies.perfect
        else:
            first = strategies.perfect
            second = strategies.human
        g = game.Game(first, second)
        g.play_game(display=True)
        again = get_input("Would you like to play again (y or n)?", ("y", "n"))


if __name__ == "__main__":
    main()
