"""
Import dependencies
"""
from flask import Blueprint, jsonify, request
from src.service.auth_service import AuthService
from src.middleware.auth import generate_token


class AuthController:
    """
    This class represents the authentication controller.

    It provides methods to handle authentication-related operations.
    """

    def __init__(self, auth_service: AuthService):
        """
        Initializes a new instance of the AuthController class.

        Args:
            auth_service (AuthService): An instance of AuthService.

        Returns:
            None
        """
        self.auth_service = auth_service
        self.blueprint = Blueprint('auth_controller_blueprint', __name__)

        self.blueprint.add_url_rule(
            '/login',
            view_func=self.login,
            methods=['POST']
        )

    def login(self):
        """
        Login with email dan password
        ---
        parameters:
            - name: body
              in: body
              required: true
              schema:
                type: object
                properties:
                  email:
                    type: string
                    description: masukan email disini
                    required: true
                  password:
                    type: string
                    description: masukan password disini
                    required: true
        responses:
            200:
              description: Logged in successfully
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  message:
                    type: string
                  status:
                    type: string
                  data:
                    type: object
        Returns:
            A success message with a token.
        """
        # Get user
        payload = request.get_json()
        email = payload['email']
        password = payload['password']

        user = self.auth_service.login(email, password)
        token = generate_token(email)
        if user:
            return {
                'code': 200,
                'message': 'Logged in successfully',
                'status': 'success',
                'data': {
                    'user': user,
                    'token': token
                }
            }
        else:
            return {
                'code': 401,
                'message': 'Invalid credentials',
                'status': 'error',
                'data': {}
            }

    def logout(self):
        """
        Logs out the current user.

        Returns:
            None
        """
        # Check if the Authorization header exists
        token = request.headers.get('Authorization', None)

        # If no token is provided, return a 400 Bad Request response
        if not token:
            return jsonify({'message': 'No token provided'}), 400

        # Invalidate the token (optional)
        # In a stateless JWT-based authentication system, tokens are typically invalidated by the client
        # For demonstration purposes, you can simply return a message
        # indicating successful logout

        # Here you might add additional logic to perform any necessary cleanup
        # or logging out on the server side

        return jsonify({'message': 'Successfully logged out'})
