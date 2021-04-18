import re
from passlib.hash import pbkdf2_sha512


class Utils:
    @staticmethod
    def username_is_valid(username: str) -> bool:
        """
        A username must start with a letter and can only contain alpha-numeric characters.
        """
        pattern = re.compile(r'^[A-Za-z]+[A-Za-z0-9]*$')
        return pattern.match(username)

    @staticmethod
    def password_is_valid(password: str) -> bool:
        """
        A password must 
        (1) have at least one number.
        (2) have at least one uppercase and one lowercase character.
        (3) have at least one special character.
        (4) contain at least eight characters.
        """
        pattern = re.compile(
            r'^(?=.{8,32}$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!"#$%&\'()*+-./:;<=>?@[\]^_`{|} ~,\\]).*')
        return pattern.match(password)

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Implement the SHA512-Crypt password hash.
        """
        return pbkdf2_sha512.hash(password)

    @staticmethod
    def check_hashed_password(password: str, hashed_password: str) -> bool:
        """
        Verify the password.
        """
        return pbkdf2_sha512.verify(password, hashed_password)
