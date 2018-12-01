class UserErrors(Exception):
    def __init__(self,message):
        self.message = message

    def error_code(self):
        pass

class InvalidPhoneError(UserErrors):
    def error_code(self):
        return 100

class UserNotExistError(UserErrors):
    def error_code(self):
        return 101

class UserAlreadyExistError(UserErrors):
    def error_code(self):
        return 102
