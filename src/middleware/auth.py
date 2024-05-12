"""
This function will be as middleware, protected unauthenticated users
"""
import os
from functools import wraps
from flask import jsonify, request
import jwt

# Define your secret key for JWT
# Replace this with your actual secret key
secret_key = os.getenv("SECRET_KEY")

# Define middleware function to authenticate JWT token
def authenticate_token(f):
    """
    This function will be handle auth token
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the Authorization header is present
        if 'Authorization' not in request.headers:
            return jsonify({'message': 'Authorization header is missing'}), 401

        # Get the JWT token from the Authorization header
        token = request.headers.get('Authorization', '').split(' ')[1]

        # If no token is provided, return 401 Unauthorized
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            # Verify the JWT token
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            # Set the user object in the request and call the route function
            request.user = data
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token is expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(*args, **kwargs)

    return decorated_function

# Define function to generate JWT token
def generate_token(email):
    """
    This function generates a JWT token for the given user ID
    """
    # Create payload with user ID
    payload = {'email': email}
    # Generate JWT token with the secret key
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    # Return the token as a string
    return token
