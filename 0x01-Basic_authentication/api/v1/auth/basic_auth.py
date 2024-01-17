#!/usr/bin/env python3
"""
Basic Authentication module
"""

from api.v1.auth.auth import Auth
import base64
import binascii


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
