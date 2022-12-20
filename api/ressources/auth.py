from flask import request, jsonify, make_response
from os import environ as env
from functools import wraps


# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if "access-token" in request.headers:
            token = request.headers["access-token"]
        if not token:  # throw error if no token provided
            return make_response(
                jsonify({"message": "A valid access-token is missing!"}), 401
            )
        if token == env.get("TOKEN"):
            return f(*args, **kwargs)
        return make_response(jsonify({"message": "invalid access-token"}), 401)

    return decorator
