#!/usr/bin/env python3
"""
auth.py
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    _hash_password
    Args:
        password (str):
    Returns:
        bytes:
    """
    # converting password to array of bytes
    bytes = password.encode('utf-8')
    # generating the salt
    salt = bcrypt.gensalt()
    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)
    return hash
