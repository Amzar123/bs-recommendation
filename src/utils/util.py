from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

class Util:
    _app = None
    _db = None
    _migrate = None

    @staticmethod
    def get_app():
        if Util._app is None:
            Util._app = Flask(__name__)
            Util._app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/database_name'
        return Util._app

    @staticmethod
    def get_db():
        if Util._db is None:
            Util._db = SQLAlchemy(Util.get_app())
        return Util._db

    @staticmethod
    def get_migrate():
        if Util._migrate is None:
            Util._migrate = Migrate(Util.get_app(), Util.get_db())
        return Util._migrate
