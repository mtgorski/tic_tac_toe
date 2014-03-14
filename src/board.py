'''
This module defines a class for representing the board in a game of tic-tac-toe.
'''


class Board(object):
    '''
    Instances of this class represent a board for playing tic-tac-toe.

    *Constructor arguments: none
    '''
    # Locations on the board are indexed as follows:
    # 0 | 1 | 2
    #--------------
    # 3 | 4 | 5
    #--------------
    # 6 | 7 | 8
    winners = (['x','x','x'], ['o','o','o'])

    def __init__(self):
        self.board = [str(i) for i in range(9)]

    def place(self, index, play):
        '''
        Places the play on the board at the index.

        *Arguments
        index: an integer 0 through 8
        play: the strings "x" or "o"

        *Raises: IndexError if index is already occupied
        '''
        pass

    def result(self):
        '''
        *Returns:
        "x" or "o" if "x" or "o" has won
        "Tie" if the game is over and neither has won
        "None" if the game is not over
        '''
        pass

    @property
    def rows(self):
        '''
        Gets a list of the rows on the board.
        '''
        return [ [self.board[i], self.board[i+1], self.board[i+2]]
                 for i in range(0, 9, 3) ]

    @property
    def columns(self):
        '''
        Gets a list of the columns on the board.
        '''
        pass

    @property
    def diagonals(self):
        '''
        Gets a list of the diagonals on the board (left to right first,
        right to left second).
        '''
        pass

    def __str__(self):
        rows = self.rows
        row_strings = (" " + " | ".join(rows[i]) for i in range(3))
        return "\n-----------\n".join(row_strings)
