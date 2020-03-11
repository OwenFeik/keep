import keyring
import gkeepapi
import getpass

keep = gkeepapi.Keep()

def get_session(email, password = None, user = False):
    token = keyring.get_password('google-keep-token', email)
    if token:
        keep.resume(email, token)
        return keep

    if not password:
        if user:
            password = getpass.getpass('Enter your password > ')
        else:
            raise SystemExit
        
    try:
        keep.login(email, password)
    except gkeepapi.exception.LoginException as e:
        print(f'Error logging in: {e}')
        raise SystemExit
    
    token = keep.getMasterToken()
    keyring.set_password('google-keep-token', email, token)

    return keep
