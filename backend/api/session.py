import secrets

class SessionManager:
    def __init__(self):
        self.users = {}
    
    # TODO: Make token expire after some time

    # Adds a session for the user and returns a token, or None if invalid.
    def add_user(self, email):
        if self.users.get(email) is not None:
            return None
        
        token = secrets.token_hex(32)

        self.users[email] = token
        return token
    
    # Return true if the user has a valid session.
    def validate_user(self, email, token):
        user = self.users.get(email)
        if user is None:
            return False
        return user.token == token
