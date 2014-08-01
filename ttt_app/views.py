from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
import json

from ttt_app.board import Board
from ttt_app.strategies import perfect

def play(request):
    '''
    A request handler responsible for rendering the game board html and
    passing the required information to game-handling javascript.
    '''
    player_first = request.POST.get('player_first')
    if player_first is None and request.method == 'GET':
        player_first = 'true'
    elif player_first is None:
        player_first = 'false'
    context = {'player_first' : player_first,
               'advance_url' : reverse("3T:advance_start")}
    return render(request, 'ttt_app/board.html', context)


def advance_start(request):
    '''
    An empty handler to aid with reverse url resolution.
    '''
    return HttpResponse()


def advance(request, player_first, board):
    '''
    A request handler that mediates between the javascript game logic
    and the backend game strategy code. Given a game state, the response
    returns the AI's next move, if any, and the result of the game, if any.

    :param player_first: string representing whether the player went first
        ('true' or false')
    :param board: string representing the state of the board. Length 9 each
        character being 'x', 'o' or '-'
    :returns: JSON response of the form {'board' : '-x--o----', 'wins' : ''},
        where 'wins' can be either '', 'x', 'o' or 'tie'.
    '''
    response = advance_helper(player_first, board)
    return HttpResponse(json.dumps(response), content_type="application/json")


def advance_helper(player_first, board_string):
    '''
    Given a game state represented by a string, updates that state
    with the perfect strategy's next move, if any and the result
    of the game, if any.

    :param player_first: string representing whether the player went first
        ('true' or false')
    :param board: string representing the state of the board. Length 9 each
        character being 'x', 'o' or '-'
    :returns: dictionary of the form {'board' : '-x--o----', 'wins' : ''},
        where 'wins' can be either '', 'x', 'o' or 'tie'.
    '''
    board = construct_board(board_string)
    result = board.result()
    if result == "None":
        move = perfect(board)
        board.place(*move)
        board_string = construct_board_str(board)
        result = board.result()
        if result == "None":
            result = ''
    result = result.lower()
    return {'board' : board_string, 'wins': result}


def construct_board_str(board):
    '''
    Constructs a string representation of a board from a tic-tac-toe
    board object.

    :param board: board.Board instance
    :returns: string length 9, each character being 'x', 'o' or '-'
    '''
    result = []
    for i in board.board:
        if i in ('x', 'o'):
            result.append(i)
        else:
            result.append('-')
    return ''.join(result)


def construct_board(board_str):
    '''
    Constructs a tic-tac-toe board from a string representing the board.

    :param board_str: length 9 string, each character being in -, x or o>

    :returns: board.Board object
    '''
    board_initializer = range(9)
    for index, value in enumerate(board_str):
        if value in ('x', 'o'):
            board_initializer[index] = value
    return Board(board_initializer)


def launch(request):
    '''
    :returns: response with the page for launching a game of tic-tac-toe.
    '''
    return render(request, 'ttt_app/launch.html')