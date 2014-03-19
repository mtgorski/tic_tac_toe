'''
This module defines various strategies for playing tic-tac-toe.

A strategy is function that, given a state of the board, returns
a play (a tuple of the form (board index, play), where play is 'x' or 'o').
'''
import random



# This random strategy will facilitate testing game logic
# and the perfect strategy.

def random_strat(board):
    '''
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
