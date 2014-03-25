'''
Python 2.7

This module contains the main program logic.
'''


def get_input(prompt, options=None):
    '''
    Asks the user for input, using the prompt. If options are specified,
    repeats the question until the answer is in the options.

    *Arguments
    prompt (str): the phrase displayed to the user when asking for input
    
    '''
    while True:
        answer = raw_input(prompt+"  ")
        if options and answer not in options:
            print "That's not a valid input."
            print "Valid options are: "+", ".join(options)+".\n"
        else:
            break
    return answer
