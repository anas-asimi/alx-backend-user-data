#!/usr/bin/env python3
"""
Main file
"""
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def hello_world():
    """hello world"""
    payload = {"message": "Bienvenue"}
    return jsonify(payload)


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """users"""
    email, password = request.form.get("email"), request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """login"""
    email, password = request.form.get("email"), request.form.get("password")
    if AUTH.valid_login(email, password):
        new_session = AUTH.create_session(email)
        payload = {"email": email, "message": "logged in"}
        resp = make_response(jsonify(payload))
        resp.set_cookie('session_id', new_session)
        return resp
    abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """logout"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(session_id)
    return redirect('/')


@app.route("/profile", strict_slashes=False)
def profile():
    """profile"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    payload = {"email": user.email}
    return jsonify(payload)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """get_reset_password_token"""
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
        payload = {"email": email, "reset_token": reset_token}
        return jsonify(payload)
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """update_password"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
        payload = {"email": email, "message": "Password updated"}
        return jsonify(payload)
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
