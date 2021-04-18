from uuid import uuid4
from typing import Dict
from models.model import Model
from common.utils import Utils
import models.user.errors as errors


class User(Model):
    """
    Create user instances and interacts with collection users.
    """
    collection = 'users'

    def __init__(self, username: str, password: str, _id: str = None) -> None:
        self.username = username
        self.password = password
        self._id = _id or uuid4().hex

    @classmethod
    def find_by_username(cls, username: str) -> 'User':
        """
        Search the database using the username.
        """
        try:
            return cls.find_one_by(username=username)
        except TypeError:
            raise errors.UserNotFoundError(
                'The username you have entered does not match any account.')

    @classmethod
    def is_login_valid(cls, username: str, password: str) -> bool:
        """
        Verify the login is valid.
        """
        user = cls.find_by_username(username=username)

        if not Utils.check_hashed_password(password, user.password):
            raise errors.IncorrectPasswordError(
                'The password you have entered is incorrect.')
        return True

    @classmethod
    def register_user(cls, username: str, password: str) -> bool:
        """
        Register a new user.
        """
        if not Utils.username_is_valid(username):
            raise errors.InvalidUserNameError(
                'A username must start with a letter and can only contain alpha-numeric characters.')

        if not Utils.password_is_valid(password):
            raise errors.InvalidPasswordError(
                'A password must (1) have at least one number. (2) have at least one uppercase and one lowercase character. (3) have at least one special character. (4) contain at least eight characters.')

        try:
            # If find the username, it means the user already exists.
            cls.find_by_username(username)
            raise errors.UserAlreadyRegisteredError(
                'The username you used to register already exists.')
        except errors.UserNotFoundError:
            # Hash the password user entered before saving to mongndb
            User(username, Utils.hash_password(password)).save_to_mongo()
        return True

    def json(self) -> Dict:
        return {"_id": self._id,
                "username": self.username,
                "password": self.password}
