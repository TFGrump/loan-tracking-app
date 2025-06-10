import hashlib
import re

from flask import Response


class Authorization:
    def __init__(self, db_handler):
        self.error_message = ""
        self.db_handler = db_handler
    
    def is_matching_password(self, pass_one, pass_two):
        return self.is_valid_password(pass_one) and pass_one == pass_two
    
    def is_valid_password(self, password):
        # Check to see if the password fits all the required minimums
        # At least 1 lowercase letter
        # At least 1 upper case letter
        # At least 1 number
        # At least 1 special charater
        # At least 8 charaters
        # Does not contain any special characters that would cause SQL injection
        if len(password) > 8:
            return False
        if '\\' in password or ';' in password:
            return False
        for regex in ['[[:lower:]]', '[[:upper:]]', '[[:digit:]]', '[^[:alpha:][:digit:]]']:
            res = re.search(regex, password)
        return False


class PasswordReset(Authorization):
    def __init__(self, db_handler):
        super().__init__(db_handler)

    def update_password(self, email, password):
        return None


class Register(Authorization):
    def __init__(self, db_handler):
        super().__init__(db_handler)

    def register(self, username, pass_one, pass_two):
        if self.is_matching_password(pass_one, pass_two):
            self.db_handler.insert()


class Login(Authorization):
    def __init__(self, db_handler):
        super().__init__(db_handler)

    def valid_login(self, username, password):
        print(username, password)
        # Verify password
        # Get auth token
        response = Response(status=200)
        response.set_cookie('auth_token', 'auth_token_test')
        return response
    
    def get_error_message(self):
        message = self.error_message
        self.error_message = ""
        return message

    def set_error(self, message):
        self.error_message = message
