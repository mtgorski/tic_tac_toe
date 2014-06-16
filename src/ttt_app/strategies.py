'''
This module defines various strategies for playing tic-tac-toe.

A strategy is function that, given a state of the board, returns
a play (a tuple of the form (board index, play), where play is 'x' or 'o').
'''
import random
import copy
import cPickle


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
Otherwise, the board is unacceptable. 

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
    play = board.next_play
    indices = board.open_indices
    if not indices:
        raise ValueError, "there are no plays to make on this boad"
    for index in indices:
        new_board = copy.deepcopy(board)
        new_board.place(index, play)
        if is_acceptable(new_board, play):
            return index, play
    # This final return should never be executed in a normal game
    # but rather only if a board on which the perfect strategy
    # had not been playing is passed in. 
    return indices[0], play 


def memoize_mutable(f):
    '''
    A wrapper for memoizing functions with mutable parameters.
    '''
    memo = {}
    def _f(*args, **kws):
        arg_str = cPickle.dumps(args)+cPickle.dumps(kws)
        result = memo.get(arg_str)
        if result:
            return result
        result = f(*args, **kws)
        memo[arg_str] = result
        return result
    return _f


@memoize_mutable
def is_acceptable(board, player):
    '''
    Determines whether the board is acceptable to a player, i.e.,
    whether it is possible to avoid losing given that board.

    *Arguments
    board (board.Board instance): the board to be determined acceptable or not
    player (str): 'x' or 'o', the symbol the player uses
    '''
    result = board.result()
    if result == player or result == 'Tie':
        return True
    elif result == "None":
        pass
    else:
        return False
    next_player = board.next_play
    if next_player == player:
        next_board = copy.deepcopy(board)
        next_board.place(*perfect(board))
        return is_acceptable(next_board, player)
    else:
        for next_board in board.next_boards():
            if not is_acceptable(next_board, player):
                return False
        return True
    return False


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





