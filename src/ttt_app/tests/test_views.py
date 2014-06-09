from django.test.utils import setup_test_environment
from django.test import TestCase, Client
from django.http import HttpResponseNotAllowed

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from board import Board
from strategies import perfect
from views import construct_board


class PlayFunction(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = '/play'
        setup_test_environment()

    def test_postRequestUsesBoardTemplate(self):
        post_data = {'player_first':'true'}
        response = self.client.post(self.url, post_data)
        template = 'ttt_app/board.html'
        self.assertTemplateUsed(response, template)

    def test_getRequestRaises405(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response, HttpResponseNotAllowed)

    def test_playerFirstWithtNoBoardReturnsResponseContextWithEmptyBoard(self):
        post_data = {'player_first':'true'}
        response = self.client.post(self.url, post_data)
        expected = Board()
        actual = response.context['board_object']
        self.assertEqual(expected, actual)

    def test_AIFirstWithNoBoardReturnsResponseContextWithOneMove(self):
        post_data = {'player_first':'false'}
        response = self.client.post(self.url, post_data)
        board = Board()
        ai_move = board.place(*perfect(board))
        actual = response.context['board_object']
        self.assertEqual(actual, board)

    


class ConstructBoardFunction(TestCase):

    def setUp(self):
        self.post_dict = dict(('board{}'.format(n), '-') for n in range(9))

    def test_normalUse1(self):
        result = construct_board(self.post_dict)
        expected = Board()
        self.assertEqual(result, expected)

    def test_normalUse2(self):
        self.post_dict['board0'] = 'x'
        result = construct_board(self.post_dict)
        init_board = range(9)
        init_board[0] = 'x'
        expected = Board(init_board)
        self.assertEqual(expected, result)