'''
This module contains the test suite for the game logic.
'''


import unittest

from game import Game
from strategies import random_strat


class TestGame(unittest.TestCase):

    def setUp(self):
        self.game1 = Game(random_strat, random_strat, "A", "B")

    def test_game(self):

        self.assertEqual(self.game1.result, 'None')
        self.game1.play_game()
        result = self.game1.result
        self.assertIn(result, ("Tie", "x", "o"))
        if result == "Tie":
            self.assertEqual(self.game1.winner, "No one")
        else:
            self.assertIn(self.game1.winner, ("A", "B"))
        self.assertRaises(ValueError, self.game1.play_game)


class TestGameRepeatedly(TestGame):
    def test_repeatedly(self):
        for i in xrange(100):
            super(TestGameRepeatedly, self).setUp()
            super(TestGameRepeatedly, self).test_game() 
    
        
if __name__ == "__main__":
    unittest.main()
    
