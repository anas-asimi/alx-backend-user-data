#!/usr/bin/env python3
"""
auth.py
"""

from db import DB
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid

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


def _generate_uuid() -> str:
    """_generate_uuid"""
    new_uuid = uuid.uuid1()
    return str(new_uuid)


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
            self._db._session.add
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
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
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Create session ID
        Args:
            email (str):
        """
        assert isinstance(email, str) and len(email) > 0
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            self._db._session.commit()
            return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Find user by session ID
        Args:
            session_id (str):
        """
        if session_id is None:
            return
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy session
        Args:
            user_id (int):
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            self._db._session.commit()
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """get_reset_password_token"""
        try:
            user = self._db.find_user_by(email=email)
            user.reset_token = _generate_uuid()
            self._db._session.commit()
            return user.reset_token
        except NoResultFound:
            raise ValueError("no user")

    def update_password(self, reset_token: str, password: str) -> None:
        """update_password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            user.hashed_password = _hash_password(password)
            user.reset_token = None
            self._db._session.commit()
        except NoResultFound:
            raise ValueError("no user")
