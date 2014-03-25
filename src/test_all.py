'''
This module combines all test suites and runs them if executed as __main__.
'''
import unittest

import test_board
import test_game
import test_strategies


def suite():
    modules = [test_board, test_game, test_strategies]
    suites = [m.suite() for m in modules]
    return unittest.TestSuite(suites)


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
