from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.template import RequestContext

from board import Board
from strategies import perfect

# Create your views here.
def play(request):
    '''
    The view handles the playing of a game of tic-tac-toe. Expects a post
    request.
        -Post must have the key 'player_first' with value 'true' or 'false'
        -If the post comes from the ttt_app/board.html form it
            must have keys 'board<n>' for n in range(9) with values 'x', 'o' or '-'
        -If the post comes from here it must also have the
            key 'choice' with value '<n>' with n in range(9)

    *Returns:
        -If the game is still in progress after the AI move and/or player move
        returns an HttpResponse with the template ttt_app/board.html rendered
        with the context {'board_object':<Board instance>}
    '''
    # Only allow post requests b/c we always need info about the game
    # being played
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    try:
        board = construct_board(request.POST)
        index = int(request.POST['choice'])
        play = board.next_play
        board.place(index, play)
        result = board.result()
        if result in ('x', 'o', 'Tie'):
            return HttpResponseRedirect('/results')
        board.place(*perfect(board))
        result = board.result()
        if result in ('x', 'o', 'Tie'):
            return HttpResponseRedirect('/results')
    # KeyError will be raised by construct_board if the post request
    # lacks the key 'board<n>' for some n in range(9), indicating
    # that the game has just been launched or that a faulty post
    # has been made
    except KeyError:
        board = Board()
        if request.POST['player_first'] == 'false':
            board.place(*perfect(board))
    context = {'board_object':board}
    return render(request, 'ttt_app/board.html', context)


def construct_board(post_dict):
    '''
    Constructs a tic-tac-toe board from a dictionary representing a post request.

    *Returns: Board object
    *Raises: KeyError if there's not sufficient information to reconstruct the board
    '''
    board = range(9)
    for i in range(9):
        key = 'board{}'.format(i)
        value = post_dict[key]
        if value in ('x', 'o'):
            board[i] = value
    return Board(board)


def results(request):
    '''
    Displays the results of a game.
    '''
    return HttpResponse('The game is over.')