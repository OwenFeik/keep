import json

def load_config():
    with open('config.json', 'r') as cf:
        return json.load(cf)

def save_config():
    with open('config.json', 'w') as cf:
        json.dump(config, cf, indent = 4)

try:
    config = load_config()
except FileNotFoundError:
    config = {
        'email': '',
        'todo-list-id': ''
    }
    save_config()
