'''
This module contains a function for getting input from the user.
'''

def get_input(prompt, options=None):
    '''
    Asks the user for input, using the prompt. If options are specified,
    repeats the question until the answer is in the options.

    *Arguments
    prompt (str): the phrase displayed to the user when asking for input
    options (collection): container of valid inputs as strings
    
    '''
    while True:
        answer = raw_input(prompt+"  ")
        if options and answer not in options:
            print "That's not a valid input."
            print "Valid options are: "+", ".join(options)+".\n"
        else:
            break
    return answer
