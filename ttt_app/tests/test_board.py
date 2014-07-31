'''
Contains the test suite for the Board class from board.py
'''

import unittest
import sys
import inspect

import os


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from ttt_app.board import Board



class ConstructorMethodBoardClass(unittest.TestCase):

    def test_RaisesTypeErrorIfBoardArgumentCantBeConvertedToList(self):
        self.assertRaises(TypeError, Board, 1)

    def test_IterableBoardArgumentConvertedToList(self):
        arg = (0, 1, 2, 3, 4, 5, 6, 'o', 'x')
        board = Board(arg)
        self.assertEqual(board.board, [0, 1, 2, 3, 4, 5, 6, 'o', 'x'])

    def test_BoardArgumentTooShortRaisesValueError(self):
        arg = [0, 1, 2, 3]
        self.assertRaises(ValueError, Board, arg)

    def test_BoardArgumentTooLongRaisesValueError(self):
        arg = range(10)
        self.assertRaises(ValueError, Board, arg)

    def test_BoardArgumentWithInvalidElementRaisesValueError(self):
        arg = [0, "1", 2, 3, 4, 5, 6, 7, 8]
        self.assertRaises(ValueError, Board, arg)

    def test_BoardArgumentWithInvalidElementRaisesValueError2(self):
        arg = [0, 1, 2, None, 3, 4, 5, 6, 7, 8]
        self.assertRaises(ValueError, Board, arg)

    def test_BoardArgumentWithInvalidElementRaisesValueError3(self):
        arg = [0, 's', 2, 3, 4, 5, 6, 7, 8]
        self.assertRaises(ValueError, Board, arg)

    def test_BoardArgumentWithIndexOutOfOrderRaisesValueError(self):
        arg = [1, 1, 2, 3, 4, 5, 6, 7, 8]
        self.assertRaises(ValueError, Board, arg)

    def test_BoardArgumentWithInvalidGameStateRaisesValueError(self):
        arg = ['x', 'x', 2, 3, 4, 5, 6, 7, 8]
        self.assertRaises(ValueError, Board, arg)
        

class Helper(object):

    def set_boards(self):
        self.board1 = Board()
        self.board2 = Board([0, "x", "o", 3, "x", 5, "o", 7, 8])
    

class RowsAttributeBoardClassTest(unittest.TestCase, Helper):

    def setUp(self):
        self.set_boards()

    def test_OnEmptyBoardReturnsListOfRows(self):
        self.assertEqual(self.board1.rows, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])

    def test_OnPopulatedBoardReturnsListOfRows(self):
        self.assertEqual(self.board2.rows, [[0, "x", "o"], [3, "x", 5], ["o", 7, 8]])


class ColumnsAttributeBoardClassTest(unittest.TestCase, Helper):

    def setUp(self):
        self.set_boards()

    def test_OnEmptyBoardReturnsListOfColumns(self):
        self.assertEqual(self.board1.columns, [[0, 3, 6], [1, 4, 7], [2, 5, 8]])

    def test_OnPopulatedBoardReturnsListOfColumns(self):
        self.assertEqual(self.board2.columns, [[0, 3, "o"], ["x", "x", 7], ["o", 5, 8]])


class DiagonalsAttributeBoardClassTest(unittest.TestCase, Helper):

    def setUp(self):
        self.set_boards()

    def test_OnEmptyBoardReturnsListOfDiagonals(self):
        self.assertEqual(self.board1.diagonals, [[0, 4, 8], [2, 4, 6]])

    def test_OnPopulatedBoardReturnsListOfDiagonals(self):
        self.assertEqual(self.board2.diagonals, [[0, 'x', 8], ['o', 'x', 'o']])


class OpenIndicesAttributeBoardClassTest(unittest.TestCase, Helper):

    def setUp(self):
        self.set_boards()

    def test_OnEmptyBoardReturnsListOfAllIndices(self):
        self.assertEqual(self.board1.open_indices, range(9))

    def test_OnPopulatedBoardReturnsListOfIndicesWithNoPlays(self):
        self.assertEqual(self.board2.open_indices, [0, 3, 5, 7, 8])


class ComparisonOperatorBoardClassTest(unittest.TestCase):

    def setUp(self):
        self.board1 = Board(['o', 'x', 2, 'x', 'x', 'o', 6, 'o', 8])
        self.board2 = Board(['x', 'o', 'o', 'x', 'x', 'o', 'o', 'x', 'x'])
        self.board3 = Board(['x', 'o', 'o', 'x', 'x', 'o', 'o', 'x', 'x'])
        
    def test_OnBoardWithDifferentFirstElementComparedBasedOnFirstElement(self):
        self.assertLess(self.board1, self.board2)

    def test_OnBoardsWithSameElementTreatedEqual(self):
        self.assertEqual(self.board2, self.board3)

    
class ResultMethodBoardClassTest(unittest.TestCase):

    def assertResultReturnsStringNone(self, board):
        result = board.result()
        self.assertEqual(result, 'None')

    def assertResultReturnsPlay(self, board, play):
        result = board.result()
        self.assertEqual(result, play)

    def test_OnEmptyBoardReturnsTheStringNone(self):
        board = Board()
        self.assertResultReturnsStringNone(board)

    def test_OnUnfinishedGameBoardReturnsTheStringNone(self):
        board = Board([0, 'x', 'o', 3, 'x', 5, 'o', 7, 8])
        self.assertResultReturnsStringNone(board)

    def test_OnBoardWonByXOnColumnReturnsStringx(self):
        board = Board([0, "x", "o", 3, "x", 5, "o", "x", 8])
        self.assertResultReturnsPlay(board, 'x')

    def test_OnBoardWonByXOnDiagonalReturnsStringx(self):
        board = Board(["x", "x", "o", 3, "x", 5, "o", "o", "x"])
        self.assertResultReturnsPlay(board, 'x')
        
    def test_OnBoardWonByOOnDiagonalReturnsStringo(self):
        board = Board(['x', "x", "o", 3, "o", 5, "o", "x", 8])
        self.assertResultReturnsPlay(board, 'o')

    def test_OnBoardWonByXOnRowReturnsStringx(self):
        board = Board(["x", "x", "x", 3, "o", 5, "o", "o", 8])
        self.assertResultReturnsPlay(board, 'x')

    def test_OnBoardWithTieReturnsStringTie(self):
        board = Board(["x", "x", "o", "o", "o", "x", "x", "o", "x"])
        result = board.result()
        self.assertEqual(result, 'Tie')
        

class PlaceMethodBoardClassTest(unittest.TestCase):

    def test_OnEmptyBoardAssignsPlayToIndex(self):
        board = Board()
        board.place(8, 'x')
        self.assertEqual(board, Board([0, 1, 2, 3, 4, 5, 6, 7, 'x']))

    def test_OnSemiPopulatedBoardAssignsPlayToIndex(self):
        board = Board([0, "x", "o", 3, "x", 5, "o", 7, 8])
        board.place(7, 'x')
        self.assertEqual(board, Board([0, 'x', 'o', 3, 'x', 5, 'o', 'x', 8]))


class NextPlayAttributeBoardClassTest(unittest.TestCase):

    def assertNextPlayEquals(self, board, play):
        next_play = board.next_play
        self.assertEqual(next_play, play)

    def test_OnEmptyBoardReturnsStringx(self):
        self.assertNextPlayEquals(Board(), 'x')

    def test_OnEmptyBoardDefaultOverridenReturnsStringo(self):
        self.assertNextPlayEquals(Board(x_first=False), 'o')

    def test_OnXFirstWithOneXReturnsStringo(self):
        self.assertNextPlayEquals(Board([0, 1, 2, 3, 'x', 5, 6, 7, 8]), 'o')

    def test_OnXFirstWithEqualXOReturnsStringx(self):
        self.assertNextPlayEquals(Board(['x', 'o', 2, 3, 4, 5, 6, 7, 8]), 'x')

    def testOnOFirstWithOneOReturnsStringx(self):
        self.assertNextPlayEquals(Board(['o', 1, 2, 3, 4, 5, 6, 7, 8], x_first=False), 'x')

    def testOnOFirstWithEqualXOReturnsStringo(self):
        self.assertNextPlayEquals(Board(['o', 'x', 2, 3, 4, 5, 6, 7, 8], x_first=False), 'o')

    def testOnFullBoardReturnsNone(self):
        self.assertNextPlayEquals(Board(['x', 'o', 'o', 'x', 'x', 'o', 'x', 'o', 'x']), None)
        

class NextBoardsMethodBoardClassTest(unittest.TestCase):

    def test_OnEmptyBoardReturns9Boards(self):
        board = Board()
        result = board.next_boards()
        self.assertEqual(len(result), 9)

    def test_OnFullBoardReturnsNoBoards(self):
        board = Board(['o', 'x', 'x', 'x', 'x', 'o', 'o', 'o', 'x'])
        result = board.next_boards()
        self.assertEqual(result, [])

    def test_OnBoardWithTwoOptionsReturnsListOfBothResultingBoards(self):
        board = Board([0, 1, 'x', 'o', 'x', 'o', 'x', 'o', 'x'])
        result = board.next_boards()
        expected1 = Board(['o', 1, 'x', 'o', 'x', 'o', 'x', 'o', 'x'])
        expected2 = Board([0, 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x'])
        self.assertEqual(sorted([expected1, expected2]), sorted(result))
                        

    def test_DoesNotMutateBoard(self):
        board = Board(['o', 1, 2, 3, 'x', 5, 6, 7, 8])
        board.next_boards()
        new_board = Board(['o', 1, 2, 3, 'x', 5, 6, 7, 8])
        self.assertEqual(board, new_board)
        




def suite():
    test_classes = [NextBoardsMethodBoardClassTest,
                    NextPlayAttributeBoardClassTest,
                    PlaceMethodBoardClassTest,
                    ResultMethodBoardClassTest,
                    ComparisonOperatorBoardClassTest,
                    OpenIndicesAttributeBoardClassTest,
                    DiagonalsAttributeBoardClassTest,
                    ColumnsAttributeBoardClassTest,
                    RowsAttributeBoardClassTest,
                    ConstructorMethodBoardClass
                    ]
    suites = [unittest.TestLoader().loadTestsFromTestCase(test_class)
              for test_class in test_classes]
    return unittest.TestSuite(suites)
    


