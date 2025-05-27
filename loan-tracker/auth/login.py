class Login:
    def __init__(self):
        self.error_message = ""

    def valid_login(self, username, password):
        print(username, password)
        return False
    
    def get_error_message(self):
        message = self.error_message
        self.error_message = ""
        return message

    def set_error(self, message):
        self.error_message = message
