class UserError(Exception):
    """
    UserError save error messages. Other subclass errors inherit from it.
    """

    def __init__(self, message):
        self.message = message


class UserNotFoundError(UserError):
    pass


class UserAlreadyRegisteredError(UserError):
    pass


class InvalidUserNameError(UserError):
    pass


class InvalidPasswordError(UserError):
    pass


class IncorrectPasswordError(UserError):
    pass
