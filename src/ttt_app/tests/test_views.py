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

    def response_to_new_game_post(self, player_first=True):
        '''
        Returns the response made when a new game is started.
        '''
        value = 'true' if player_first else 'false'
        post_data = {'player_first': value}
        return self.client.post(self.url, post_data)

    def test_postRequestUsesBoardTemplate(self):
        response = self.response_to_new_game_post()
        template = 'ttt_app/board.html'
        self.assertTemplateUsed(response, template)

    def test_getRequestRespondsWithEmptyBoardStringInContext(self):
        response = self.client.get(self.url)
        expected = '012345678'
        actual = response.context['board_str']
        self.assertEqual(actual, expected)

    def test_playerFirstWithtNoBoardReturnsResponseContextWithEmptyBoardString(self):
        response = self.response_to_new_game_post()
        expected = '012345678'
        actual = response.context['board_str']
        self.assertEqual(expected, actual)

    def test_AIFirstWithNoBoardReturnsResponseContextWithOneMove(self):
        response = self.response_to_new_game_post(player_first=False)
        board = Board()
        board.place(*perfect(board))
        expected = ''.join(str(i) for i in board.board)
        actual = response.context['board_str']
        self.assertEqual(actual, expected)

    def test_PlayerMoveOnEmptyBoardReturnsResponseContextWithPlayerAndAIFirstMove(self):
        post_data = {'board_str': '-'*9}
        post_data['player_first'] = 'true'
        post_data['choice0'] = 'X'
        response = self.client.post(self.url, post_data)
        # Player makes a move at 0, then perfect moves at 4
        expected = 'x123o5678'
        actual = response.context['board_str']
        self.assertEqual(actual, expected)

    def test_PlayerMakesGameEndingMoveRedirectsToResults(self):
        post_data = {'board_str': 'xoxooxox-'}
        post_data['player_first'] = 'true'
        post_data['choice8'] = 'X'
        response = self.client.post(self.url, post_data)
        self.assertRedirects(response, '/results')

    def test_AIMakesGameEndingMoveRedirectsToResult(self):
        post_data = {'board_str': 'oxxxx-oo-'}
        post_data['player_first'] = 'false'
        post_data['choice5'] = 'O'
        response = self.client.post(self.url, post_data)
        self.assertRedirects(response, '/results')

    def test_TemplateContainsInputTagDescribingWhoWentFirst1(self):
        response = self.response_to_new_game_post(player_first=True)
        tag = '<input type=\"hidden\" name=\"player_first\" value=\"true\">'
        self.assertContains(response, tag, html=True)

    def test_TemplateContainsInputTagDescribingWhoWentFirst2(self):
        response = self.response_to_new_game_post(player_first=False)
        tag = '<input type=\"hidden\" name=\"player_first\" value=\"false\">'
        self.assertContains(response, tag, html=True)

    def test_TemplateContainsInputTagDescribingTheBoard1(self):
        response = self.response_to_new_game_post()
        tag = '<input type=\"hidden\" name=\"board_str\" value=\"012345678">'
        self.assertContains(response, tag, html=True)

    def test_TemplateContainsInputTagDescribingTheBoard2(self):
        response = self.response_to_new_game_post(player_first=False)
        # construct the string representing the board after the
        # perfect strategy plays
        board = [str(i) for i in range(9)]
        index, play = perfect(Board())
        board[index] = play
        board_str = ''.join(board)
        tag = '<input type=\"hidden\" name=\"board_str\" value=\"{}\">'.format(board_str)
        self.assertContains(response, tag, html=True)

    def test_TemplateHasTagForEachPlayOnTheBoard1(self):
        response = self.response_to_new_game_post(player_first=False)
        tag = '<td class=\"xo\">X</td>'
        self.assertContains(response, tag, 1, html=True)

    def test_TemplateHasTagForEachPlayOnTheBoard2(self):
        board = Board([0, 1, 2, 3, 'x', 5, 6, 7, 8])
        board_str = '0123x5678'
        post_data = {'board_str':board_str, 'player_first':'false',
                     'choice0': 'O'}
        response = self.client.post(self.url, post_data)
        # the view will place the user's O and then the ai's x
        tag = '<td class=\"xo\">X</td>'
        self.assertContains(response, tag, 2, html=True)

    def test_TemplateHasSubmitTagForOpenPlay1(self):
        response = self.response_to_new_game_post()
        tag = '<input type=\"submit\" class=\"btn btn-info xobutton\" value=\"X\" name=\"choice0\">'
        self.assertContains(response, tag, 1, html=True)

    def test_TemplateHasSubmitTagForOpenPlay2(self):
        response = self.response_to_new_game_post(player_first=False)
        tag = '<input type=\"submit\" class=\"btn btn-info xobutton\" value=\"O\" name=\"choice8\">'
        self.assertContains(response, tag, 1, html=True)


class ConstructBoardFunction(TestCase):

    def setUp(self):
        self.post_dict = {'board_str': '-'*9}

    def test_normalUse1(self):
        result = construct_board(self.post_dict)
        expected = Board()
        self.assertEqual(result, expected)

    def test_normalUse2(self):
        self.post_dict['board_str'] = 'x--------'
        result = construct_board(self.post_dict)
        init_board = range(9)
        init_board[0] = 'x'
        expected = Board(init_board)
        self.assertEqual(expected, result)

