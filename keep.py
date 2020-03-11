import gkeepapi
import re
import difflib
import sys

import config
import session
import utils


if not config.config['email']:
    config.config['email'] = input('Google keep email > ').lower().strip()
    config.save_config()

keep = session.get_session(config.config['email'])

text = ''
title = ''

# -f: File
if '-f' in sys.argv:
    file_name = utils.get_argv('-f')

    try:
        with open(file_name, 'r') as file:
            text = file.read()
            title = sys.argv[1]
    except FileNotFoundError:
        print(f'File {file_name} not found.')

# -t: Title
if '-t' in sys.argv:
    t = utils.get_argv('-t', arg_required = False, failure_message = 'No title supplied for -t, ignoring flag.')
    if t:
        title = t

# -D: toDo
if '-D' in sys.argv:
    list_name = utils.get_argv('-D')
    try:
        config.config['todo-list-id'] = keep.find(func = utils.match_title(list_name))[0].id
    except IndexError:
        print(f'List {list_name} not found. Unable to update default to do list.')

# -d: toDo
if '-d' in sys.argv:
    list_name = utils.get_argv('-d', arg_required = False)

    if not list_name:
        list_id = config.config['todo-list-id'] 
        if list_id:
            todo = keep.get(list_id)
            if todo:
                print(todo)
            else:
                if utils.get_decision(f'Couldn\'t find default list. Remove as default?'):
                    config.config['todo-list-id'] = ''
                    config.save_config()
                raise SystemExit
        else:
            todo_lists = keep.find(query = re.compile(r'[Tt][Oo] *[Dd][Oo]'), func = lambda n: type(n) == gkeepapi.node.List)
    else:
        todo_lists = keep.find(func = lambda n: type(n) == gkeepapi.node.List and n.title.lower() == list_name.lower())

    if not todo_lists:
        print(f'No to do lists found.')
        raise SystemExit

    for note in todo_lists:
        print(note)
        print('\n')

# -g: Get
if '-g' in sys.argv:
    note_name = utils.get_argv('-g')

    notes = keep.find(func = utils.match_title(note_name))
    if notes:
        for note in notes:
            print(note)
    else:
        names = [n.title for n in keep.all()]
        try:
            suggestion = difflib.get_close_matches(note_name, names, 1)[0]
            print('Couldn\'t find a note named "{note_name}". Perhaps you meant "{suggestion}"?')
        except IndexError:
            print('Couldn\'t find a note named "{note_name}".')
            raise SystemExit
