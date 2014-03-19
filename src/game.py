'''
This module defines a class for representing games of tic-tac-toe.
'''

import copy

from board import Board


class Game(object):
    '''
    Instances of this class represent a game of tic-tac-toe.

    *Constructor Arguments:
    strategy_A (function): the strategy that goes first
    strategy_B (function): the strategy that goes second
    strategy_A_name (str; default=the function's name): the name given to
        the first strategy
    strategy_B_name (str; default=the function's name): the name given to
        the second strategy
    x_first (bool; default=True): determines whether 'x' goes first
    '''
    # Instance attribute history can be used
    # to examine the history of the game. It is a list of the form
    # [board, (strategy, play), board, (strategy, play) ....board]

    # self.winner accesses the name of the winning strategy or
    # "No one" if there was a tie. It is not set until the game
    # has ended. 

    def __init__(self, strategy_A, strategy_B, strategy_A_name="",
                 strategy_B_name="", x_first=True):
        self.strategy_A = strategy_B
        self.strategy_B = strategy_A
        self.strategy_A_name = (strategy_A.__name__ if not strategy_A_name
                               else strategy_A_name)
        self.strategy_B_name = (strategy_B.__name__ if not strategy_B_name
                               else strategy_B_name)
        
        self.x_first = x_first
        self.board = Board(x_first = self.x_first)

        self.history = [] 
        
        
    def play_game(self, display=False):
        '''
        Plays a game of tic-tac-toe between the instance's two strategies.
        Sets self.result to "Tie", "x" or "o".
        Sets self.winner to the name of one of the strategy or to "No one"
        if the game is a tie. 

        *Arguments:
        display(bool; default=False): if True, the board and each play are printed
        during the game

        *Raises:
        ValueError if the game is over
        '''
        
        if self.result != 'None':
            raise ValueError, "Game has already been played"
        current = self.strategy_A
        up_next = self.strategy_B
        if self.x_first:
            names = {'x' : self.strategy_A_name, 'o' : self.strategy_B_name}
        else:
            names = {'o':  self.strategy_A_name, 'x' : self.strategy_B_name}

        while self.result == 'None':
            self.history.append(copy.deepcopy(self.board))
            if display:
                print self.board
                print "\n"
            play = current(self.board)
            self.board.place(*play)
            self.history.append((names[play[1]], play))
            if display:
                name = names[play[1]]
                print "%s plays %s at %i.\n"%(name, play[1], play[0])
            current, up_next = up_next, current
            
        self.history.append(copy.deepcopy(self.board))
        result = self.result
        if result == "Tie":
            self.winner = "No one"
        else:
            self.winner = names[result]

        if display:
            print self.board
            print "\n"
            if result == "Tie":
                print "It's a tie!\n"
            else:
                print self.winner + " wins!\n"

    def display_history(self):
        '''
        Displays the sequence of boards and moves played thus far.
        '''
        for item in self.history:
            if isinstance(item, Board):
                print item
                print "\n"
            else:
                print "%s plays %s at %i.\n"%(item[0], item[1][1], item[1][0])
        
    @property
    def result(self):
        '''
        Gets the result of the game: 'x' or 'o' or 'Tie'. If
        the game is not over, 'None'.
        '''
        return self.board.result()


if __name__ == "__main__":
    import strategies
    g = Game(strategies.random_strat, strategies.random_strat, "A", "B")
    g.play_game()
