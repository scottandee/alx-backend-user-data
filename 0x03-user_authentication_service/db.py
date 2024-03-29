#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from typing import Dict

from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a user to the DB
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **filter_param: Dict) -> User:
        """
        Find a user by a certain parameter
        """
        try:
            user = self._session.query(User).filter_by(**filter_param).first()
        except InvalidRequestError:
            raise InvalidRequestError
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **updates: Dict) -> None:
        """
        Update a user
        """
        user_attrs = [
            "hashed_password", "email",
            "session_id", "reset_token"
        ]
        for key in updates.keys():
            if key not in user_attrs:
                raise ValueError
        user = self.find_user_by(id=user_id)
        for key, value in updates.items():
            setattr(user, key, value)
        self._session.commit()
