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

    def test_PlayerMoveOnEmptyBoardReturnsResponseContextWithPlayerAndAIFirstMove(self):
        post_data = dict(('board{}'.format(n), '-') for n in range(9))
        post_data['player_first'] = 'true'
        post_data['choice'] = '0'
        response = self.client.post(self.url, post_data)
        # Player makes a move at 0, then perfect moves at 4
        expected = Board(['x', 1, 2, 3, 'o', 5, 6, 7, 8])
        actual = response.context['board_object']
        self.assertEqual(actual, expected)

    def test_PlayerMakesGameEndingMoveRedirectsToResults(self):
        post_data = {'board0':'x', 'board1': 'o', 'board2': 'x',
                     'board3': 'o', 'board4': 'o', 'board5': 'x',
                     'board6': 'o', 'board7': 'x', 'board8': '-'}
        post_data['player_first'] = 'true'
        post_data['choice'] = '8'
        response = self.client.post(self.url, post_data)
        self.assertRedirects(response, '/results')

    def test_AIMakesGameEndingMoveRedirectsToResult(self):
        post_data = {'board0':'o', 'board1': 'x', 'board2': 'x',
                     'board3': 'x', 'board4': 'x', 'board5': '-',
                     'board6': 'o', 'board7': 'o', 'board8': '-'}
        post_data['player_first'] = 'false'
        post_data['choice'] = '5'
        response = self.client.post(self.url, post_data)
        self.assertRedirects(response, '/results')




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