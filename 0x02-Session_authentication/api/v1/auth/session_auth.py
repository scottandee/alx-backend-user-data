#!/usr/bin/env python3
"""
Session Authentication module
"""

from api.v1.auth.auth import Auth
from models.user import User
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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ user_id_for_session_id
        Retreive a User id based on session

        Returns:
          - None if session_id is None, or not a string
          - user_id of session
        """
        if session_id is None or not isinstance(session_id, str):
            return
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ current_user
        Defines the current user

        Returns:
          - current user
          - None
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)
