#!/usr/bin/env python3
"""
Basic Authentication module
"""

from api.v1.auth.auth import Auth
import base64
import binascii
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Basic Authentication Class
    """
    def extract_base64_authorization_header(
                self, authorization_header: str
            ) -> str:
        """ extract_base64_authorization_header
        Extracts username and password from authorization
        header

        Returns:
          - None if authorization header is none, not a string, or if
            string doesn't start with Basic
          - The value after "Basic"
        """
        if authorization_header is None:
            return
        if not isinstance(authorization_header, str):
            return
        if authorization_header[:6] != "Basic ":
            return
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
            ) -> str:
        """ decode_base64_authorization_header
        decode the authorization header with base64

        Returns:
          - None if base64_authorization_header is None,
            not a string, or is not valid base64
          - The decoded value as UTF8 string
        """
        if base64_authorization_header is None:
            return
        if not isinstance(base64_authorization_header, str):
            return
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode("utf-8")
        except binascii.Error:
            return

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> (str, str):
        """ extract_user_credentials
        extract email and password from base64 decoded string

        Returns
          - (None, None) if decoded_base64_authorization_header is
            None, not a string, doesn't contain `:`
          - Tuple of user email and password
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        credentials: (str, str) = tuple(
            decoded_base64_authorization_header.split(":")
        )
        return credentials

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        """ user_object_from_credentials
        returns user instance based on email and password or
        None
        """
        if user_email is None or user_pwd is None:
            return
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return
        user = User.search({"email": user_email})
        print(len(user))
        if len(user) == 0:
            return
        if user[0].is_valid_password(user_pwd):
            return user[0]
        return
