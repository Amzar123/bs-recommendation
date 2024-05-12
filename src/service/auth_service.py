"""
Import repository
"""
from src.repository.user_repository import User, UserRepository

class AuthService: 
    """
    This class implement for auth
    """
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def login(self, email: str, password: str):
        """
        This function to handle login process
        """
        user = self.user_repo.get_user_by_email(email)
        if user and user.password == password:
            return user
        return None

    def register(self, email: str, password: str):
        """
        This function handle registration process
        """
        user = User(email=email, password=password)
        return self.user_repo.add_user(user)
