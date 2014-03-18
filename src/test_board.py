'''
Contains the test suite for the Board class from board.py
'''

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
