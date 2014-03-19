'''
This module defines a class for representing games of tic-tac-toe.
'''



class Game(object):
    '''
    Instances of this class represent a game of tic-tac-toe.

    *Constructor Arguments:
    strategy_A (function): the strategy that goes first
    strategy_B (function): the strategy that goes second
    x_first (bool; default=True): determines whether 'x' goes first
    '''

    def __init__(self, strategy_A, strategy_B, x_first=True):
        pass

    def play_game(self, display=False):
        '''
        Plays a game of tic-tac-toe between the instance's two strategies.

        *Arguments:
        display(bool; default=False): if True, the board and each play are printed
        during the game

        *Raises:
        ValueError if the game is over
        '''
        pass

    def display_history(self):
        '''
        Displays the sequence of boards and moves played thus far.
        '''
        pass
        
    @property
    def result(self):
        '''
        Gets the result of the game: 'x' or 'o' or 'Tie'. If
        the game is not over, 'None'.
        '''
        pass
