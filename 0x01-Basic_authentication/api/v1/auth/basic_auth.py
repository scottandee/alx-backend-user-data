#!/usr/bin/env python3
"""
Basic Authentication module
"""

from api.v1.auth.auth import Auth
import base64


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
            decoded string doesn't start with Basic
          - The value after "Basic"
        """
        if authorization_header is None:
            return
        if not isinstance(authorization_header, str):
            return
        if authorization_header[:6] != "Basic ":
            return
        return authorization_header[6:]
