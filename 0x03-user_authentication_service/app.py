#!/usr/bin/env python3
"""
Main file
"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    """
    hello world
    """
    payload = {"message": "Bienvenue"}
    return jsonify(payload)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
