#!/usr/bin/env python3
"""Authentication Module
"""

import bcrypt
import uuid
from sqlalchemy.orm.exc import NoResultFound
from user import User
from db import DB


def _hash_password(password: str) -> bytes:
    """_hash_password
    This function encrypts a password

    Parameters:
      @password: The password to be encrypted

    Returns:
      - Hashed password
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt)


def _generate_uuid() -> str:
    """ _generate_uuid
    This function generates a new uuid

    Returns:
      - string representation of a new uuid
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register_user
        This function registers a new user and saves details
        to the database

        Parameters:
          @email: user's email
          @password: user's password

        Returns:
          - The created user
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hash_pwd = _hash_password(password)
            user = self._db.add_user(email, hash_pwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """valid_ login
        This function checks if the login credentials provided
        are valid

        Parameters:
          @email: user's email
          @password: user's password

        Returns:
          - True if credentials are valid
          - False if credentials are not valid
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed_pwd = user.hashed_password
            if bcrypt.checkpw(password.encode("utf-8"), hashed_pwd):
                return True
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """create_session
        This function creates a new session id

        Parameter:
        @email: user's email

        Returns:
          - string representation of session id
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user_id=user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
