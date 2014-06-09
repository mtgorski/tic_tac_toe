from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed
from django.template import RequestContext

from board import Board
from strategies import perfect

# Create your views here.
def play(request):
    '''
    The view handles the playing of a game of tic-tac-toe. Expects a post
    request.
        -Post must have the key 'player_first' with value 'true' or 'false'
        -Post can have keys 'board<n>' for n in range(9) with values 'x', 'o' or '-'
    '''
    # Only allow post requests b/c we always need info about the game
    # being played
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    if request.POST['player_first'] == 'true':
        board = Board()
    else:
        board = Board()
        board.place(*perfect(board))
    context = {'board_object':board}
    return render(request, 'ttt_app/board.html', context)


def construct_board(post_dict):
    '''
    Constructs a tic-tac-toe board from a dictionary representing a post request.

    *Returns: Board object
    *Raises: MultiKeyValueError if the post is not sufficient to describe the board
    '''
    board = range(9)
    for i in range(9):
        key = 'board{}'.format(i)
        value = post_dict[key]
        if value in ('x', 'o'):
            board[i] = value
    return Board(board)