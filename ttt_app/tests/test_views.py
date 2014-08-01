import sys
import inspect

from django.test.utils import setup_test_environment
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
import os


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from ttt_app.board import Board
from ttt_app.strategies import perfect
from views import construct_board, advance_helper


class Helper(object):

    def setup_client(self):
        self.client = Client()
        setup_test_environment()

    def assertResponseContextContainsKeyValue(self, response, key, value):
        '''
        Checks that the key, value pair is in the response's context.
        '''
        context = response.context
        expected = {key: value}
        self.assertDictContainsSubset(expected, context)

class PlayFunction(TestCase, Helper):

    urls = "test_urls"


    def setUp(self):
        self.setup_client()
        self.template = 'ttt_app/board.html'
        self.url = reverse('3T:play')

    ###################################################################
    # Helper methods
    ###################################################################

    def response_to_new_game_post(self, player_first=True):
        '''
        Returns the response made when a new game is started via
        a post request with no board information.
        '''
        post_data = {'player_first': 'true'} if player_first else {}
        return self.client.post(self.url, post_data)

    ###################################################################
    # Tests
    ###################################################################

    def test_postRequestUsesBoardTemplate(self):
        response = self.response_to_new_game_post()
        self.assertTemplateUsed(response, self.template)


    ###################################################################
    # Testing the board template
    ###################################################################

    def test_WhenPlayerGoesFirstTemplateAssociatesPlayerWithX(self):
        response = self.response_to_new_game_post()
        text = 'Player (X)'
        self.assertContains(response, text)

    def test_WhenAIGoesFirstTemplateAssociatesAIWithX(self):
        response = self.response_to_new_game_post(player_first=False)
        text = 'Perfect (X)'
        self.assertContains(response, text)

    def test_WhenPlayerGoesFirstTemplateAssociatesAIWithO(self):
        response = self.response_to_new_game_post()
        text = 'Perfect (O)'
        self.assertContains(response, text)

    def test_WhenAIGoesFirstTemplateAssociatesPlayerWithO(self):
        response = self.response_to_new_game_post(player_first=False)
        text = 'Player (O)'
        self.assertContains(response, text)


class AdvanceHelperFunctionTest(TestCase, Helper):


    def test_OnEmptyBoard_ReturnsFirstMove(self):
        result = advance_helper('false', '---------')
        self.assertDictContainsSubset({'board': 'x--------'}, result)

    def test_OnEmptyBoard_NoOneWins(self):
        result = advance_helper('false', '---------')
        self.assertDictContainsSubset({'wins': ''}, result)

    def test_OnMidGameBoard_UpdatesBoardWithNextMove1(self):
        result = advance_helper('true', 'o---xx---')
        self.assertDictContainsSubset({'board' : 'o--oxx---'}, result)

    def test_OnMidGameBoard_UpdatesBoardWithNextMove2(self):
        result = advance_helper('false', 'xxo-o----')
        self.assertDictContainsSubset({'board' : 'xxo-o-x--'}, result)

    def test_OnMidGameBoard_NoOneWins(self):
        result = advance_helper('true', 'o---xx---')
        self.assertDictContainsSubset({'wins' : ''}, result)

    def test_OnTiePassedIn_ReportsTie(self):
        result = advance_helper('false', 'xxoooxxxo')
        self.assertDictContainsSubset({'wins' : 'tie'}, result)

    def test_OnXWinPassedIn_ReportsXWin(self):
        result = advance_helper('false', 'xxxoo----')
        self.assertDictContainsSubset({'wins': 'x'}, result)

    def test_OnOWinPassedIn_ReportsOWin(self):
        result = advance_helper('true', 'oooxx-x--')
        self.assertDictContainsSubset({'wins': 'o'}, result)



class ConstructBoardFunction(TestCase):


    def test_normalUse1(self):
        result = construct_board('---------')
        expected = Board()
        self.assertEqual(result, expected)

    def test_normalUse2(self):
        result = construct_board('x--------')
        init_board = range(9)
        init_board[0] = 'x'
        expected = Board(init_board)
        self.assertEqual(expected, result)


class LaunchFunction(TestCase, Helper):

    urls = "test_urls"

    def setUp(self):
        self.setup_client()
        self.url = reverse('3T:launch')

    def response_to_get(self):
        return self.client.get(self.url)

    def test_getRequestReturnsResponseUsingLaunchTemplate(self):
        template = 'ttt_app/launch.html'
        self.assertTemplateUsed(self.response_to_get(), template)

    def test_getRequestReturnsResponseUsingBaseTemplate(self):
        template = 'ttt_app/base.html'
        self.assertTemplateUsed(self.response_to_get(), template)

    def test_getRequestReturnsResponseWithFormToPostToPlayFunction(self):
        play_url = reverse("3T:play")
        tag = '<form method=\"post\" action=\"{0}\">'.format(play_url)
        self.assertContains(self.response_to_get(), tag, 1)

    def test_getRequestReturnsResponseWithCheckboxToGoFirst(self):
        tag = '<input type=\"checkbox\" name=\"player_first\" value=\"true\">'
        self.assertContains(self.response_to_get(), tag, 1, html=True)
