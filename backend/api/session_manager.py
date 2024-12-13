import logging, secrets

logger = logging.getLogger(__name__)

class SessionManager:
    def __init__(self, database):
        self.users = {}
        self.database = database
    
    # TODO: Make token expire after some time

    # Adds a session for the user and returns a token, or None if invalid.
    def add_authorized_user(self, id, email):
        existing_user = self.users.get(email)
        if existing_user is not None:
            return existing_user['token']
        
        token = secrets.token_hex(32)

        self.users[email] = {
            'id': id,
            'token': token
        }
        return token
    
    # Return the User if they are authenticated, otherwise return None
    def get_authorized_user(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        arr = auth_header.split(',')
        if (len(arr) != 2):
            return None

        email = arr[0]
        token = arr[1]
            
        user = self.users.get(email)
        if user is None:
            return None
        if user['token'] != token:
            return None
        
        database_user = self.database.lookup_user(user['id'])
        return database_user
    