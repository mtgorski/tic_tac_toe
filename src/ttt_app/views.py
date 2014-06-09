from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

from board import Board

# Create your views here.
def play(request):
    context = {}
    return render(request, 'ttt_app/board.html', context)