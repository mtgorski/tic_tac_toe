from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.template import RequestContext

from board import Board
from strategies import perfect

# Create your views here.
def play(request):
    '''
    The view handles the playing of a game of tic-tac-toe. If the request method
    is a post:
        -Post must have the key 'player_first' with value 'true' or 'false'
        -If the post comes from the ttt_app/board.html form it
            must have the 'board' with value <str, length 9, elements in range(9) or
            'x' or 'o'>
        -If the post comes from here it must also have the
            key 'choice<n>' with value 'X' or 'O' with n in range(9)
    If the request method is a get:
        -Assumes the player is going first and starts a game
    *Returns:
        -If the game is still in progress after the AI move and/or player move
        returns an HttpResponse with the template ttt_app/board.html rendered
        with the context {'board_object':<Board instance>,
        'player_first': <'true' or 'false'> }
    '''
    # Only allow post requests b/c we always need info about the game
    # being played
    player_first = request.POST.get('player_first')
    if player_first is None and request.method == 'GET':
        player_first = 'true'
    try:
        board = construct_board(request.POST)
        choice_key = filter(lambda x: x.startswith('choice'), request.POST.keys())[0]
        index = int(choice_key[-1])
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
        if  player_first == 'false':
            board.place(*perfect(board))
    board_str = ''.join(str(i) for i in board.board)
    next_play = board.next_play.upper()
    context = {'board_object':board, 'player_first': player_first,
               'board_str': board_str, 'next_play': next_play}
    return render(request, 'ttt_app/board.html', context)


def construct_board(post_dict):
    '''
    Constructs a tic-tac-toe board from a string representing the board
    in a post request.

    Expects post_dict['board_str'] = <length 9 str, each entry being -, x or o>

    *Returns: Board object
    *Raises: KeyError if there's not sufficient information to reconstruct the board
    '''
    post_board = post_dict['board_str']
    board_initializer = range(9)
    for index, value in enumerate(post_board):
        if value in ('x', 'o'):
            board_initializer[index] = value
    return Board(board_initializer)


def results(request):
    '''
    Displays the results of a game.
    '''
    return HttpResponse('The game is over.')