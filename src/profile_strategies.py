'''
This module profiles the perfect strategy.
'''

import cProfile


import strategies
import game


def play_games(calls):
    '''
    Plays calls number of games between the perfect strategy and
    a random strategy.

    *Arguments
    calls (int): number of games
    '''
    for _ in xrange(calls):
        g = game.Game(strategies.perfect, strategies.random_strat)
        g.play_game()


def profile(calls):
    '''
    Runs a profile on calls number of games between a random strategy
    and a perfect strategy.
    '''
    cProfile.run("play_games(%i)"%calls)


if __name__ == "__main__":
    profile(100)

'''
Prior to caching

>>> profile(100)


46144146 function calls (40827757 primitive calls) in 38.067 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   38.067   38.067 <string>:1(<module>)
   461632    0.510    0.000    0.510    0.000 board.py:106(diagonals)
   418068    0.453    0.000    0.801    0.000 board.py:115(next_play)
   190962    0.133    0.000    0.133    0.000 board.py:27(__init__)
   486059    0.438    0.000    0.438    0.000 board.py:37(place)
   461632    2.600    0.000    6.191    0.000 board.py:52(result)
    77397    0.761    0.000    1.343    0.000 board.py:70(next_boards)
   209330    0.377    0.000    0.377    0.000 board.py:82(open_indices)
   461632    1.355    0.000    1.708    0.000 board.py:90(rows)
   461632    1.150    0.000    1.373    0.000 board.py:98(columns)
5020049/295297    9.831    0.000   26.776    0.000 copy.py:145(deepcopy)
  2108930    0.314    0.000    0.314    0.000 copy.py:198(_deepcopy_atomic)
   295297    1.959    0.000    7.753    0.000 copy.py:226(_deepcopy_list)
   295297    1.382    0.000    3.649    0.000 copy.py:234(_deepcopy_tuple)
   295297    0.933    0.000   13.327    0.000 copy.py:253(_deepcopy_dict)
  3290118    3.367    0.000    4.470    0.000 copy.py:267(_keep_alive)
   295297    1.731    0.000   22.513    0.000 copy.py:306(_reconstruct)
   295297    0.171    0.000    0.279    0.000 copy_reg.py:92(__newobj__)
        1    0.000    0.000    0.000    0.000 copy_reg.py:95(_slotnames)
      892    0.002    0.000    0.014    0.000 game.py:109(result)
      100    0.001    0.000    0.001    0.000 game.py:31(__init__)
      100    0.004    0.000   38.066    0.381 game.py:46(play_game)
        1    0.001    0.001   38.067   38.067 profile_strategies.py:12(play_games)
      246    0.001    0.000    0.001    0.000 random.py:271(choice)
131687/346    0.715    0.000   37.975    0.110 strategies.py:28(perfect)
460740/444    1.829    0.000   37.926    0.085 strategies.py:58(is_acceptable)
      246    0.001    0.000    0.003    0.000 strategies.py:90(random_strat)
   295297    0.108    0.000    0.108    0.000 {built-in method __new__ of type object at 0x100180f20}
   590594    0.358    0.000    0.358    0.000 {getattr}
   295298    0.344    0.000    0.344    0.000 {hasattr}
  9786652    0.953    0.000    0.953    0.000 {id}
   885891    0.285    0.000    0.285    0.000 {isinstance}
   295297    0.112    0.000    0.112    0.000 {issubclass}
   590840    0.092    0.000    0.092    0.000 {len}
   295297    1.687    0.000    1.687    0.000 {method '__reduce_ex__' of 'object' objects}
  6139937    1.443    0.000    1.443    0.000 {method 'append' of 'list' objects}
   836136    0.348    0.000    0.348    0.000 {method 'count' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
  8605464    1.330    0.000    1.330    0.000 {method 'get' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 {method 'get' of 'dictproxy' objects}
   295297    0.064    0.000    0.064    0.000 {method 'iteritems' of 'dict' objects}
      246    0.000    0.000    0.000    0.000 {method 'random' of '_random.Random' objects}
   295297    0.164    0.000    0.164    0.000 {method 'update' of 'dict' objects}
  1218661    0.761    0.000    0.761    0.000 {range}
'''
