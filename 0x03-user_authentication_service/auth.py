#!/usr/bin/env python3
"""Authentication Module
"""

import bcrypt


def _hash_password(password: str):
    """_hash_password
    This function encrypts a password

    Parameters:
      - @password: The password to be encrypted

    Returns:
      - Hashed password
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt)
