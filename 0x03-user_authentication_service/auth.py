#!/usr/bin/env python3
"""
auth.py
"""

from db import DB
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound

# generating the salt
salt = bcrypt.gensalt()


def _hash_password(password: str) -> bytes:
    """
    _hash_password
    Args:
        password (str):
    Returns:
        bytes:
    """
    # converting password to array of bytes
    bytes = password.encode('utf-8')
    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)
    return hash


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        register_user
        Args:
            email (str):
            password (str):
        """
        assert isinstance(email, str) and len(email) > 0
        assert isinstance(password, str) and len(password) > 0
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> User:
        """
        valid_login
        Args:
            email (str):
            password (str):
        """
        assert isinstance(email, str) and len(email) > 0
        assert isinstance(password, str) and len(password) > 0
        try:
            user = self._db.find_user_by(email=email)
            hashed_password = _hash_password(password)
            if hashed_password == user.hashed_password:
                return True
            return False
        except NoResultFound:
            return False
