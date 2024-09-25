#!/usr/bin/env python3
"""
Main file
"""
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
