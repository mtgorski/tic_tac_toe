'''
Contains the test suite for tic-tac-toe strategies.
'''

import unittest
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from strategies import random_strat, is_acceptable, perfect, human
from board import Board
from game import Game


class RandomStratFunctionTest(unittest.TestCase):

    def setUp(self):
        self.empty = Board()
        self.empty_o = Board(x_first=False)
        self.test1 = Board(["o", 1, 2, 3, "x", 5, "x", 7, 8])
        self.full = Board(['x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x'])

    def test_OnEmptyBoardReturnsIndexInRange(self):
        empty_play = random_strat(self.empty)
        self.assertIn(empty_play[0], range(9))

    def test_OnEmptyBoardReturnsPlayGoingFirst1(self):
        play = random_strat(self.empty)
        self.assertEqual(play[1], "x")
        
    def test_OnEmptyBoardReturnsPlayGoingFirst2(self):
        play = random_strat(self.empty_o)
        self.assertEqual(play[1], 'o')

    def test_OnSemiFullBoardReturnsOpenIndex(self):
        play = random_strat(self.test1)
        self.assertIn(play[0], [1, 2, 3, 5, 7, 8])

    def test_OnSemiFullBoardReturnsPlayGoingNext(self):
        play = random_strat(self.test1)
        self.assertEqual(play[1], "o")

    def test_OnFullBoardRaisesValueError(self):
        self.assertRaises(ValueError, random_strat, self.full)


class HumanFunctionTest(unittest.TestCase):
    
    def test_OnFullBoardRaisesValueError(self):
        full = Board(['x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x'])
        self.assertRaises(ValueError, human, self.full)


class Helper(object):

    def set_boards(self):
        # comment denotes who goes next
        self.board1 = Board(['x', 'o', 2, 'x', 'x', 'o', 6, 7, 'o']) #x
        self.board3 = Board([0, 1, 2, 3, 'x', 5, 6, 7, 8]) #o
        self.board4 = Board(['x', 1, 2, 3, 'x', 5, 'o', 7, 8]) #o
        self.board5 = Board(['x', 1, 2, 3, 'x', 5, 'o', 'x', 'o']) #o
        self.board6 = Board(['o', 'x', 'x', 'x', 'x', 'o', 'o', 'o', 8]) #x
        self.board7 = Board(['o', 'x', 'x', 'x', 'x', 'o', 'o', 'o', 'x']) #no one
        self.board8 = Board() #x

        # These boards are acceptable to the player who goes next
        self.good_boards = [self.board1, self.board3, self.board4,
                            self.board5, self.board6, self.board8]

        self.board9 = Board(['x', 'x', 2, 'o', 'x', 5, 6, 7, 'o'])
        self.board10 = Board(['o', 'o', 2, 'x', 'x', 'x', 6, 7, 8])
        

class PerfectFunctionTest(unittest.TestCase, Helper):

    def setUp(self):
        self.set_boards()

    def test_OnBoardWithMultipleAccetableOptionsReturnsOneOfThem1(self):
        self.assertIn(perfect(self.board1), [(6, 'x'), (2, 'x')])

    def test_OnBoardWithMultipleAccetableOptionsReturnsOneOfThem2(self):
        self.assertIn(perfect(self.board3), [(0, 'o'), (2, 'o'), (6, 'o'), (7, 'o')])

    def test_OnBoardWithOneAcceptableOptionReturnsIt1(self):
        self.assertEqual(perfect(self.board4), (8, 'o'))

    def test_OnBoardWithOneAcceptableOptionReturnsIt2(self):
        self.assertEqual(perfect(self.board5), (1, 'o'))

    def test_OnBoardWithOneAcceptableOptionReturnsIt3(self):
        self.assertEqual(perfect(self.board6), (8, 'x'))

    def test_OnFullBoardRaisesValueError(self):
        self.assertRaises(ValueError, perfect, self.board7)

    # Not considering symmetries or the fact that the game can end
    # before the board is full, there are 945 ways random can play if
    # it goes first and 384 ways it can play if it goes second. 
        
    def test_InFullGameNeverLosesToRandomStrategyIfGoingFirst(self):
        results = set([])
        for _ in xrange(500):
            g = Game(perfect, random_strat)
            g.play_game()
            results.add(g.winner)
        self.assertNotIn(random_strat.__name__, results)

    def test_InFullGameNeverLosesToRandomStrategyIfGoingSecond(self):
        results = set([])
        for _ in xrange(1000):
            g = Game(random_strat, perfect)
            g.play_game()
            results.add(g.winner)
        self.assertNotIn(random_strat.__name__, results)

    def test_InFullGameTiesWhenPlayingAgainstItself(self):
        g = Game(perfect, perfect)
        g.play_game()
        self.assertEqual(g.result, "Tie")
        


class IsAcceptableFunctionTest(unittest.TestCase, Helper):

    def setUp(self):
        self.set_boards()

    def assertIsAcceptable(self, board=None, play=''):
        self.assertTrue(is_acceptable(board, play))

    def assertIsNotAcceptable(self, board=None, play=''):
        self.assertFalse(is_acceptable(board, play))

    def test_OnAcceptableBoardReturnsTrue1(self):
        self.assertIsAcceptable(self.board7, 'x')

    def test_OnAcceptableBoardReturnsTrue2(self):
        self.assertIsAcceptable(self.board9, 'x')

    def test_OnAcceptableBoardReturnsTrue3(self):
        self.assertIsAcceptable(self.board10, 'x')

    def test_OnAcceptableBoardReturnsTrue4(self):
        self.assertIsAcceptable(self.board1, 'x')

    def test_OnAcceptableBoardReturnsTrue5(self):
        self.assertIsAcceptable(self.board3, 'o')

    def test_OnAcceptableBoardReturnsTrue6(self):
        self.assertIsAcceptable(self.board4, 'o')

    def test_OnAcceptableBoardReturnsTrue7(self):
        self.assertIsAcceptable(self.board5, 'o')

    def test_OnAcceptableBoardReturnsTrue8(self):
        self.assertIsAcceptable(self.board6, 'x')

    def test_OnAcceptableBoardReturnsTrue9(self):
        self.assertIsAcceptable(self.board8, 'x')

    def test_OnUnacceptableBoardReturnsFalse1(self):
        self.assertIsNotAcceptable(self.board9, 'o')

    def test_OnUnacceptableBoardReturnsFalse2(self):
        self.assertIsNotAcceptable(self.board10, 'o')

    
    



def suite():
    test_classes = [IsAcceptableFunctionTest, PerfectFunctionTest, RandomStratFunctionTest]
    suites = [unittest.TestLoader().loadTestsFromTestCase(test_class)
              for test_class in test_classes]
    return unittest.TestSuite(suites)


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
