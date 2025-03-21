from .constants.errors import NotFoundError

class AuthHandler:

    def __init__(self, api: object, token: str) -> None:
        self.token = token
        self.api = api
        self.set_token_header(token)

    def get_token(self):

        if self.token: return self.token
        raise NotFoundError('token is not found. init the auth flow first.')
    
    def set_token_header(self, token: str) -> None:
        bearer_str = 'Bearer {token}'.format(token=token)
        self.api.headers.update({'Authorization' : bearer_str})
    
    def check_header_tokens(self):

        # If no authorization header is found, we need to include the token
        if 'Authorization' not in self.api.headers:
            token = self.get_token()
            self.set_token_header(token)