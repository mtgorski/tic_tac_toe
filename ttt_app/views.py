from django.shortcuts import render
from django.http import HttpResponse
import json

from ttt_app.board import Board
from ttt_app.strategies import perfect

# Create your views here.
def play(request):
    '''
    The view handles the playing of a game of tic-tac-toe. If the request method
    is a post:
        -Post must have the key 'player_first' with value 'true' or 'false'
        -If the post comes from the ttt_app/board.html form it
            must have the key 'board_str' with value <str, length 9, elements in range(9) or
            'x' or 'o'>
        -If the post comes from here it must also have the
            key 'choice<n>' with value 'X' or 'O' with n in range(9)
        -If the post has no key 'board_str', it begins the game
    If the request method is a get:
        -Assumes the player is going first and starts a game
    *Returns:
        -If the game is still in progress after the AI move and/or player move
        returns an HttpResponse with the template ttt_app/board.html rendered
        with the context {'board_str':<string representing the board>,
        'player_first': <'true' or 'false'>,
        'next_play' : <'X' or 'O'> }
        -If the game has ended, returns an HttpResponse with the template
        ttt_app/result.html rendered with the context
        {'player_first':<'true' or 'false'>, 'board_str': <string representing the board>,
        'result':<'x' or 'o' or 'Tie'>}
    '''
    # If there's a get request, assume the user wants to go first
    # If there's a post request with 'player_first' absent (since the
    # checkbox hasn't been used) the player goes second
    player_first = request.POST.get('player_first')
    if player_first is None and request.method == 'GET':
        player_first = 'true'
    elif player_first is None:
        player_first = 'false'

    strategy = perfect

    board_str = request.POST.get('board_str')
    # If it's not the first turn in the game...
    if board_str is not None:
        # Get the player's move and add it to the board
        board = construct_board(board_str)
        choice_key = filter(lambda x: x.startswith('choice'),
                            request.POST.keys())[0]
        index = int(choice_key[-1])
        play = board.next_play
        board.place(index, play)
        # Check the result
        result = board.result()
        # If the player's move ends the game...
        if result in ('x', 'o', 'Tie'):
            board_str = construct_board_str(board)
            context = {'result': 'Tie', 'board_str': board_str}
            return render(request, 'ttt_app/results.html', context)
        # Otherwise, add the AI's move too
        board.place(*strategy(board))
        result = board.result()
        # If the AI's move ends the game...
        if result in ('x', 'o', 'Tie'):
            board_str = construct_board_str(board)
            context = {'result': result, 'board_str': board_str}
            return render(request, 'ttt_app/results.html', context)
    # If it's the first turn in the game...
    else:
        board = Board()
        if  player_first == 'false':
            board.place(*strategy(board))

    board_str = construct_board_str(board)
    next_play = board.next_play.upper()
    context = {'player_first': player_first,
               'board_str': board_str, 'next_play': next_play}

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