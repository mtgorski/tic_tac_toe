'''
This module defines a class for representing the board in a game of tic-tac-toe.
'''


class Board(object):
    '''
    Instances of this class represent a board for playing tic-tac-toe.

    *Constructor arguments
    initial_board (default=None): an iterable representing the initial board.
        The iterable should have 9 elements, elements being either the integer corresponding
        to the index, "x" or "o"
    x_first (bool; default=True): determines whether 'x' or 'o' goes first ('x' by default)
    '''
    # Locations on the board are indexed as follows:
    # 0 | 1 | 2
    #--------------
    # 3 | 4 | 5
    #--------------
    # 6 | 7 | 8

    # The initial_board argument in the contructor is primarily for testing
    
    winners = (['x','x','x'], ['o','o','o'])

    def __init__(self, initial_board = None, x_first=True):
        if initial_board is None:
            self.board = range(9)
        else:
            length = len(initial_board)
            if length < 9:
                raise ValueError, "Too few elements in initial_board"
            if length > 9:
                raise ValueError, "Too many elements in initial_board"
            for index, element in enumerate(initial_board):
                if element in ('x', 'o'): continue
                if element in range(9) and element == index: continue
                raise ValueError, "Invalid element {}({}) in initial_board".format(element, type(element))
            initial_board = list(initial_board)
            # In a valid game, the number of x's minus the number of o's should
            # be no more than 1, and if one is greater, that play should have
            # gone first. 
            x = initial_board.count('x')
            o = initial_board.count('o')
            if x == o: pass
            elif o == x + 1 and not x_first: pass
            elif x == o + 1 and x_first: pass
            else:
                raise ValueError, "Invalid board state. Board is not the result of a valid game"
            self.board = initial_board
        if x_first:
            self.first_play = 'x'
        else:
            self.first_play = 'o'

    def place(self, index, play):
        '''
        Places the play on the board at the index.

        *Arguments
        index: an integer 0 through 8
        play: the strings "x" or "o"

        *Raises: IndexError if index is already occupied
        '''
        if self.board[index] in ("x", "o"):
            raise IndexError, "there is already a play at that index"
        self.board[index] = play
            

    def result(self):
        '''
        *Returns:
        "x" or "o" if "x" or "o" has won
        "Tie" if the game is over and neither has won
        "None" if the game is not over
        '''
        # Assumes the board is the result of a valid game. For example,
        # won't catch it if both x and o have completed rows. 
        triplets = self.rows + self.columns + self.diagonals
        for trip in triplets:
            if trip in Board.winners:
                return trip[0]
        for element in self.board:
            if element not in ("x", "o"):
                return "None"
        return "Tie"

    def next_boards(self):
        '''
        *Returns: a list of boards that are one play ahead of self.
        '''
        play = self.next_play
        result = []
        for index in self.open_indices:
            b = Board([i for i in self.board])
            b.place(index, play)
            result.append(b)
        return result

    @property
    def open_indices(self):
        '''
        Gets a list of places on the board with no plays.
        '''
        return [i for i in self.board if i not in ('x', 'o')]
        

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
        return [ [self.board[i], self.board[i+3], self.board[i+6]]
                 for i in range(3) ]

    @property
    def diagonals(self):
        '''
        Gets a list of the diagonals on the board (left to right first,
        right to left second, both going down).
        '''
        return [ [self.board[0], self.board[4], self.board[8]],
                 [self.board[2], self.board[4], self.board[6]] ]

    @property
    def next_play(self):
        '''
        Gets the next play ("x" or "o") to be placed on the board.
        '''
        x = self.board.count("x")
        o = self.board.count("o")
        if x == o:
            return self.first_play
        if x + o == 9:
            return None
        if x > o:
            return 'o'
        return 'x'
        

    def __str__(self):
        rows = self.rows
        row_strings = (" " + " | ".join([str(j) for j in rows[i]]) for i in range(3))
        return "\n-----------\n".join(row_strings)

    # Instances are compared on the basis of their boards.
    # Note however that two equivalent boards may differ
    # based on whether 'x' or 'o' went first. 
    def __cmp__(self, other):
        return cmp(self.board, other.board)


































    
