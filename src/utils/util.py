"""
It demonstrates the usage of Flask along with SQLAlchemy and Flask-Migrate for database migrations.
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Util:
    """
    Utility class for managing Flask application, database connection, and migration.

    This class provides static methods to get the Flask application instance, database connection,
    and Migrate object for the application.
    """
    _app = None
    _db = None
    _migrate = None

    @staticmethod
    def get_app():
        """
        Returns the Flask application instance.

        If the application instance does not exist,
        it creates a new instance and configures the database URI.

        Returns:
            Flask: The Flask application instance.
        """
        if Util._app is None:
            Util._app = Flask(__name__)
            Util._app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/database_name'
        return Util._app

    @staticmethod
    def get_db(app):
        """
        Get the database connection.

        Returns:
            SQLAlchemy: The database connection object.
        """
        if Util._db is None:
            db_username = os.getenv("DATABASE_USER")
            db_name = os.getenv("DATABASE_NAME")
            db_host = os.getenv("DATABASE_HOST")
            db_port = os.getenv("DATABASE_PORT")
            db_password = os.getenv("DB_PW")

            db_url = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

            # Configure database connection
            app.config['SQLALCHEMY_DATABASE_URI'] = db_url
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

            # Initialize database
            db = SQLAlchemy(app)

            Util._db = db

            return Util._db
