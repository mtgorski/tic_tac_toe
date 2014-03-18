'''
This module defines a class for representing the board in a game of tic-tac-toe.
'''


class Board(object):
    '''
    Instances of this class represent a board for playing tic-tac-toe.

    *Constructor arguments
    initial_board (default=None): a list representing the initial board.
        The list should be length 9, with entries being the integer corresponding
        to the index, "x" or "o"
    '''
    # Locations on the board are indexed as follows:
    # 0 | 1 | 2
    #--------------
    # 3 | 4 | 5
    #--------------
    # 6 | 7 | 8

    # The initial_board argument in the contructor is primarily for testing
    
    winners = (['x','x','x'], ['o','o','o'])

    def __init__(self, initial_board = None):
        if initial_board is None:
            self.board = range(9)
        else:
            self.board = initial_board

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

    def __str__(self):
        rows = self.rows
        row_strings = (" " + " | ".join([str(j) for j in rows[i]]) for i in range(3))
        return "\n-----------\n".join(row_strings)



def test_properties():

    test_board1 = Board()
    assert test_board1.rows == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    assert test_board1.columns == [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
    assert test_board1.diagonals == [[0, 4, 8], [2, 4, 6]]


    test_board2 = Board([0, "x", "o", 3, "x", 5, "o", 7, 8])
    assert test_board2.rows == [[0, "x", "o"], [3, "x", 5], ["o", 7, 8]]
    assert test_board2.columns == [[0, 3, "o"], ["x", "x", 7], ["o", 5, 8]]
    assert test_board2.diagonals == [[0, "x", 8], ["o", "x", "o"]]
    

def test_result():

    test_board1 = Board()
    assert test_board1.result() == "None"

    test_board2 = Board([0, "x", "o", 3, "x", 5, "o", 7, 8])
    assert test_board2.result() == "None"

    test_board3 = Board([0, "x", "o", 3, "x", 5, "o", "x", 8])
    assert test_board3.result() == "x"

    test_board4 = Board([0, "x", "o", 3, "o", 5, "o", "x", 8])
    assert test_board4.result() == "o"

    test_board5 = Board(["x", "x", "o", 3, "x", 5, "o", "x", "x"])
    assert test_board5.result() == "x"

    test_board6 = Board(["x", "x", "x", 3, "o", 5, "o", "o", 8])
    assert test_board6.result() == "x"

    test_board7 = Board(["o", "o", "x", "x", "x", "o", "o", "x", "o"])
    assert test_board7.result() == "Tie"


def test_place():

    test_board1 = Board()
    test_board1.place(8, "o")
    assert test_board1.board[8] == "o"

    test_board2 = Board([0, "x", "o", 3, "x", 5, "o", 7, 8])
    test_board2.place(7, "x")
    assert test_board2.result() == "x"

    

if __name__ == "__main__":
    test_properties()
    test_result()































    
