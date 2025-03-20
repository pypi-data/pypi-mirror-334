import secrets


def gen_token_key():
    key = secrets.token_urlsafe(32)
    return f'tok_{key}'
