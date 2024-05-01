"""
It demonstrates the usage of Flask along with SQLAlchemy and Flask-Migrate for database migrations.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


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
    def get_db():
        """
        Get the database connection.

        Returns:
            SQLAlchemy: The database connection object.
        """
        if Util._db is None:
            Util._db = SQLAlchemy(Util.get_app())
        return Util._db

    @staticmethod
    def get_migrate():
        """
        Returns the Migrate object for the application.

        If the Migrate object is not yet created, it creates a new one using the
        get_app() and get_db() methods.

        Returns:
            Migrate: The Migrate object for the application.
        """
        if Util._migrate is None:
            Util._migrate = Migrate(Util.get_app(), Util.get_db())
        return Util._migrate
