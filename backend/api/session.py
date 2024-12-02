import secrets

class SessionManager:
    def __init__(self):
        self.users = {}
    
    # TODO: Make token expire after some time

    # Adds a session for the user and returns a token, or None if invalid.
    def add_user(self, username, email):
        if self.users.get(username) is not None:
            return None
        
        token = secrets.token_hex(32)

        self.users[username] = {
            "email": email,
            "token": token
        }
        return token
    
    # Return true if the user has a valid session.
    def validate_user(self, username, email, token):
        user = self.users.get(username)
        if user is None:
            return False
        if user['token'] != token or user['email'] != email:
            return False
        
        return True
