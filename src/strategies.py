'''
This module defines various strategies for playing tic-tac-toe.

A strategy is function that, given a state of the board, returns
a play (a tuple of the form (board index, play), where play is 'x' or 'o').
'''
import random

'''
Here is an explanation of the "perfect" strategy.

The perfect strategy chooses any play to that leads to an acceptable board.

A board is acceptable to a player if any of the following are true:
    1) there is a tie on the board
    2) the player wins on the board
    3) It is the opponent's turn and all plays the opponent
       can make lead to an acceptable board.
    4) It is the player's turn and the play made by the
       perfect strategy on that board leads to an acceptable board.

Note that the perfect strategy has no preference for winning. It only
avoids losing.
'''

def perfect(board):
    '''
    This strategy chooses a play such that it is impossible for
    the strategy to lose, if this is possible. Otherwise it just
    picks an available play. 

    *Arguments
    board (board.Board instance): the current tic-tac-toe board

    *Returns: a tuple of the form (board index, play)

    *Raises: ValueError, if there are no plays left to make on the board
    '''
    pass


def is_acceptable(board, player):
    '''
    Determines whether the board is acceptable to a player, i.e.,
    whether it is possible to avoid losing given that board.

    *Arguments
    board (board.Board instance): the board to be determined acceptable or not
    player (str): 'x' or 'o', the symbol the player uses
    '''
    pass


# This random strategy will facilitate testing game logic
# and the perfect strategy.

def random_strat(board):
    '''
    This strategy chooses a random open location to place its move.
    
    *Arguments
    board (board.Board instance): the current tic-tac-toe board
    
    *Returns: a tuple of the form (board index, play)
    
    *Raises: ValueError, if there are no plays left to make on the board
    '''
    
    play = board.next_play
    if play is None:
        raise ValueError, "there are no plays to make on this board"
        return
    index = random.choice(board.open_indices)
    return index, play


def human(board, display=False):
    '''
    This strategy asks the user where to put the next play.

    *Arguments
    board (board.Board instance): the current tic-tac-toe board
    display (bool; default=False): determines whether the board
        should be displayed prior to asking for input

    *Returns: a tuple of the form (board index, play)

    *Raises: ValueError, if there are no plays left to make on the board
    '''
    play = board.next_play
    if play is None:
        raise ValueError, "there are no plays to make on this board"
    if display:
        print board
        print "\n"
    index = int(raw_input("Where would you like to place your %s?"%(play)))
    while index not in board.open_indices:
        print "That is not a valid location.\n"
        index = int(raw_input("Where would you like to play your %s?"%(play)))
    return index, play

