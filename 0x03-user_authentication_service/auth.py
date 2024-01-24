#!/usr/bin/env python3
"""Authentication Module
"""

import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from user import User
from db import DB


def _hash_password(password: str):
    """_hash_password
    This function encrypts a password

    Parameters:
      @password: The password to be encrypted

    Returns:
      - Hashed password
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register_user
        This function

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
