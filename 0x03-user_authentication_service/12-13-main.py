#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

user = auth.register_user(email, password)
print(user)

session_id = auth.create_session(email)
user = auth.get_user_from_session_id(session_id)
print(user)

auth.destroy_session(user.id)
user = auth.get_user_from_session_id(session_id)
print(user)
