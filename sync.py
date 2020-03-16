import keyring
import gkeepapi
import pickle

def sync(config, password = None):
    SyncSession(config, password).save()
    raise SystemExit

class SyncSession():
    def __init__(self, config, password = None):
        self.keep = gkeepapi.Keep()

        token = keyring.get_password('google-keep-token', config['email'])
        if token:
            self.keep.resume(config['email'], token)
        else:
            if not password:
                raise SystemExit
                
            try:
                self.keep.login(config['email'], password)
            except gkeepapi.exception.LoginException as e:
                print(f'Error logging in: {e}')
                raise SystemExit
    
            token = self.keep.getMasterToken()
            keyring.set_password('google-keep-token', config['email'], token)

        if config['sync-archive']:
            self.notes = self.keep.all()
        else:
            self.notes = self.keep.find(archived = False)

    def save(self):
        with open('notes.pkl', 'wb') as f:
            pickle.dump(self.notes, f)

