from django.test.utils import setup_test_environment
from django.test import TestCase, Client

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from board import Board


class PlayFunction(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = '/play'
        setup_test_environment()

    def test_getRequestUsesBoardTemplate(self):
        response = self.client.get(self.url)
        template = 'ttt_app/board.html'
        self.assertTemplateUsed(response, template)

