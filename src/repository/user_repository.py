"""
Import required dependencies 
"""
from typing import List
from sqlalchemy import  String
from sqlalchemy.orm import Session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User:
    """
    User model class.
    """
    __tablename__ = "users"
    id = db.Column(String, primary_key=True)
    email = db.Column(String, unique=True)
    password = db.Column(String)
    # Relationships
    # TODO: Add relationships here

    def __init__(self, email: str, password: str):
        """
        Initialize a User object.
        """
        self.email = email
        self.password = password

    def __repr__(self):
        """
        Return a string representation of the User object.
        """
        return f"<User {self.email}>"

class UserRepository:
    """
    Repository class for User operations.
    """

    def __init__(self, db: Session):
        """
        Initialize UserRepository with a database session.
        """
        self.db = db

    def get_user_by_email(self, email: str) -> User:
        """
        Get a user by email.
        """
        return self.db.query(User).filter(User.email == email).first()

    def add_user(self, user: User) -> User:
        """
        Add a user to the database.
        """
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_id(self, user_id: int) -> User:
        """
        Get a user by ID.
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_users(self) -> List[User]:
        """
        Get all users.
        """
        return self.db.query(User).all()

    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user by ID.
        """
        user = self.get_user_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False

    def update_user(self, user_id: int, user: User) -> User:
        """
        Update a user by ID.
        """
        user_to_update = self.get_user_by_id(user_id)
        if user_to_update:
            user_to_update.email = user.email
            user_to_update.password = user.password
            self.db.commit()
            self.db.refresh(user_to_update)
            return user_to_update
        return None
