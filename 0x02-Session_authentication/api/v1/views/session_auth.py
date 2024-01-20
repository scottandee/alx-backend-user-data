#!/usr/bin/env python3
""" Module of Users views
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from api.v1.auth.session_auth import SessionAuth
import os


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login():
    """ POST /auth_session/login/
    user login route
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    auth = SessionAuth()
    session_id = auth.create_session(user[0].id)
    response = jsonify(user[0].to_json())

    session_name = os.getenv("SESSION_NAME")

    response.set_cookie(session_name, session_id)
    return response
