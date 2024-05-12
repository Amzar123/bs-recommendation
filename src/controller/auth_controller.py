from flask import Blueprint
from src.service.auth_service import AuthService


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

    def register(self, username, password):
        """
        Registers a new user.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            None
        """
        # Implement user registration logic here
        pass

    def login(self, username, password):
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
         A success message.
        """
        # Implement user login logic here
        pass

    def logout(self):
        """
        Logs out the current user.

        Returns:
            None
        """
        # Implement user logout logic here
        pass

    def reset_password(self, username):
        """
        Resets the password for a user.

        Args:
            username (str): The username of the user.

        Returns:
            None
        """
        # Implement password reset logic here
        pass