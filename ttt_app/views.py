from django.shortcuts import render
from django.http import HttpResponse
import json

from ttt_app.board import Board
from ttt_app.strategies import perfect

# Create your views here.
def play(request):
    player_first = request.POST.get('player_first')
    if player_first is None and request.method == 'GET':
        player_first = 'true'
    elif player_first is None:
        player_first = 'false'
    context = {'player_first' : player_first}
    return render(request, 'ttt_app/board.html', context)


def advance(request, player_first, board):
    '''
    A request handler that mediates between the javascript
    game logic and the backend game strategy code. Given
    a game state, the response returns the strategy's next move,
    if any, and the result of the game, if any.
    '''
    response = advance_helper(player_first, board)
    return HttpResponse(json.dumps(response), content_type="application/json")

# There's an inexplicable problem with django trying to test
# the urls that would route advance, so this intermediate function
# exists to facilitate testing
def advance_helper(player_first, board_string):
    '''
    Given a game state represented by a strings, updates that state
    with the perfect strategy's next move, if any and the result
    of the game, if any.
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
    Constructs a string represent of a board from a tic-tac-toe board.
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

    Expects board_str = <length 9 str, each entry being in -, x or o>

    *Returns: Board object
    '''
    board_initializer = range(9)
    for index, value in enumerate(board_str):
        if value in ('x', 'o'):
            board_initializer[index] = value
    return Board(board_initializer)


def results(request):
    '''
    Displays the results of a game.
    '''
    return HttpResponse('The game is over.')


def launch(request):
    '''
    This view returns the page for launching a game of tic-tac-toe.
    '''
    return render(request, 'ttt_app/launch.html')