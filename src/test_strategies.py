'''
Contains the test suite for tic-tac-toe strategies.
'''

import unittest

from strategies import random_strat, is_acceptable, perfect, human
from board import Board
from game import Game


class TestRandom(unittest.TestCase):

    def setUp(self):
        self.empty = Board()
        self.empty_o = Board(x_first=False)
        self.test1 = Board(["o", 1, 2, 3, "x", 5, "x", 7, 8])
        self.full = Board(['x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x'])

    def test_random_strat(self):
        empty_play = random_strat(self.empty)
        self.assertIsInstance(empty_play, tuple)
        self.assertIn(empty_play[0], range(9))
        self.assertEqual(empty_play[1], ("x"))
        self.assertEqual(self.empty, Board())

        empty_play_o = random_strat(self.empty_o)
        self.assertEqual(empty_play_o[1], 'o')

        test_play = random_strat(self.test1)
        self.assertIn(test_play[0], [1, 2, 3, 5, 7, 8])
        self.assertEqual(test_play[1], 'o')

        self.assertRaises(ValueError, random_strat, self.full)

    def test_human(self):
        self.assertRaises(ValueError, human, self.full)


class TestPerfectCases(unittest.TestCase):
    '''Tests the perfect strategy against specific cases.'''

    def setUp(self):
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

    def test_acceptable(self):
        for board in self.good_boards:
            player = board.next_play
            self.assertTrue(is_acceptable(board, player))

        self.assertTrue(is_acceptable(self.board7, 'x'))
        self.assertTrue(is_acceptable(self.board7, 'o'))
        self.assertFalse(is_acceptable(self.board9, 'o'))
        self.assertTrue(is_acceptable(self.board9, 'x'))
        self.assertTrue(is_acceptable(self.board10, 'x'))
        self.assertFalse(is_acceptable(self.board10, 'o'))

    def test_perfect(self):

        self.assertIn(perfect(self.board1), [(6, 'x'), (2, 'x')])
        self.assertIn(perfect(self.board3), [(0, 'o'), (2, 'o'), (6, 'o'), (7, 'o')])
        self.assertEqual(perfect(self.board4), (8, 'o'))
        self.assertEqual(perfect(self.board5), (1, 'o'))
        self.assertEqual(perfect(self.board6), (8, 'x'))
        self.assertRaises(ValueError, perfect, self.board7)
        

class TestPerfectLossRatio(unittest.TestCase):
    '''Tests whether the perfect strategy can lose.'''

    def test_perfect(self):
        results = []
        for _ in xrange(100):
            g = Game(perfect, random_strat)
            g.play_game()
            results.append(g.winner)
        for _ in xrange(100):
            g = Game(random_strat, perfect)
            g.play_game()
            results.append(g.winner)
        self.assertNotIn(random_strat.__name__, results)

if __name__ == "__main__":
    unittest.main()
