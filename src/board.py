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
    def __cmp__(self, other):
        return cmp(self.board, other.board)


def test_properties():

    test_board1 = Board()
    assert test_board1.rows == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    assert test_board1.columns == [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
    assert test_board1.diagonals == [[0, 4, 8], [2, 4, 6]]
    assert test_board1.open_indices == [0, 1, 2, 3, 4, 5, 6, 7, 8]


    test_board2 = Board([0, "x", "o", 3, "x", 5, "o", 7, 8])
    assert test_board2.rows == [[0, "x", "o"], [3, "x", 5], ["o", 7, 8]]
    assert test_board2.columns == [[0, 3, "o"], ["x", "x", 7], ["o", 5, 8]]
    assert test_board2.diagonals == [[0, "x", 8], ["o", "x", "o"]]
    assert test_board2.open_indices == [0, 3, 5, 7, 8] 

    a = Board(['o', 'x', 2, 'x', 'x', 'o', 6, 'o', 8])
    b = Board(['x', 'o', 'o', 'x', 'x', 'o', 'o', 'o', 'x'])
    c = Board(['x', 'o', 'o', 'x', 'x', 'o', 'o', 'o', 'x'])
    assert a < b
    assert a != b
    assert b == c

    
    

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


def test_next_play():

    assert Board().next_play == "x"
    assert Board([0, 1, 2, 3, "x", 4, 5, 6, 7, 8]).next_play == "o"
    assert Board(["x", "o", 2, 3, 4, 5, 6, 7, 8]).next_play == "x"

    assert Board(x_first=False).next_play == "o"
    assert Board([0, 1, 2, 3, "x", 4, 5, 6, 7, 8], x_first=False).next_play == "o"
    assert Board(["x", "o", 2, 3, 4, 5, 6, 7, 8], x_first=False).next_play == "o"

    assert Board(['x', 'o', 'o', 'x', 'x', 'o', 'o', 'o', 'x']).next_play == None


def test_next_boards():

    test_board1 = Board(['o', 'x', 2, 'x', 'x', 'o', 6, 'o', 8])
    next1 = test_board1.next_boards()
    assert Board(['o', 'x', 'x', 'x', 'x', 'o', 6, 'o', 8]) in next1
    assert len(next1) == 3

    test_board2 = Board()
    next2 = test_board2.next_boards()
    assert len(next2) == 9
    assert test_board2 == Board() #Make sure the board wasn't mutated

    test_board3 = Board(['x', 'o', 'o', 'x', 'x', 'o', 'o', 'o', 'x'])
    next3 = test_board3.next_boards()
    assert next3 == []


if __name__ == "__main__":
    test_properties()
    test_result()
    test_place()
    test_next_play()
    test_next_boards()































    
