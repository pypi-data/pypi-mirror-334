class NotFoundError(ValueError):
    '''raise this when a variable has no value when it is expected'''

class APIError(Exception):
    '''raise this when there is an error in the API'''

    def __init__(self, error_obj):
        super().__init__(f'API Error: {error_obj.detail}. See more details in attached error object.')
        self.error = error_obj