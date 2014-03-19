'''
Contains the test suite for tic-tac-toe strategies.
'''

import unittest
from strategies import random_strat
from board import Board


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
        


if __name__ == "__main__":
    unittest.main()
