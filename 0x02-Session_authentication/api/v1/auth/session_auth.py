#!/usr/bin/env python3
"""
Session Authentication module
"""

from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """Session Authentication Class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ create_session
        Create a session for a user_id

        Returns:
          - None if user_id is None or not a string
          - session_id
        """
        if user_id is None or not isinstance(user_id, str):
            return
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id.update({session_id: user_id})
        return session_id
