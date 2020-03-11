import sys
import re

def get_argv(flag, arg_required = True, failure_message = None):
    try:
        index = sys.argv.index(flag)
        arg = sys.argv[index + 1]
    except IndexError:
        if failure_message:
            print(failure_message)
        if arg_required:
            print(f'Argument error: no argument supplied for {flag}, exiting.')
            raise SystemExit
        arg = ''

    if re.match(r'^-[\w]', arg):
        if arg_required:
            print(f'Argument error: no argument supplied for {flag}, exiting.')
            raise SystemExit
        return None
    
    return arg

def get_decision(prompt, default = 'y'):
    decision = input(f'{prompt} (default={default})> ')
    if decision == '':
        decision = default
    
    if decision in ['y', 'yes']:
        return True
    elif decision in ['n', 'no']:
        return False
    else:
        return get_decision(prompt, default)

def match_title(string):
    return lambda n: n.title.lower() == string.lower()
