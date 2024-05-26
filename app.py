"""
Import section
"""
import os
from flask import Flask, jsonify
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv


# Import controller
from src.controller.recommendation_controller import RecommendationController
from src.controller.auth_controller import AuthController

# Import repository
from src.repository.recommendation_repo import RecommendationRepo
from src.repository.student_repository import StudentRepo
from src.repository.teacher_repopsitory import TeacherRepo

# Import service
from src.service.recommendation_service import RecommendationService
from src.service.auth_service import AuthService


app = Flask(__name__)

# Load environment variables from .env
load_dotenv()

DB_USERNAME = os.getenv("DATABASE_USER")
DB_NAME = os.getenv("DATABASE_NAME")
DB_HOST = os.getenv("DATABASE_HOST")
DB_PORT = os.getenv("DATABASE_PORT")
DB_PASSWORD = os.getenv("DB_PW")

DB_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Konfigurasi koneksi database
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import db
db = SQLAlchemy(app)

# Migration
migrate = Migrate(app, db)

# Register the blueprint from the repository
recommendation_repository = RecommendationRepo(db)
student_repo = StudentRepo(db)
teacher_repo = TeacherRepo(db)

# Register the blueprint from the service
recommendation_service = RecommendationService(
    recommendation_repository, student_repo)
auth_service = AuthService(teacher_repo, student_repo)

# Register the blueprint from the controller
recommendation_controller = RecommendationController(recommendation_service)
auth_controller = AuthController(auth_service)

app.register_blueprint(
    recommendation_controller.blueprint,
    url_prefix='/recommendations')
app.register_blueprint(auth_controller.blueprint)


@app.route("/spec")
def spec():
    """
    This function is to initialize API spec
    """
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Recommendation System API"
    return jsonify(swag)


# Route to serve Swagger UI
swaggerui_blueprint = get_swaggerui_blueprint('/docs', '/spec')
app.register_blueprint(swaggerui_blueprint, url_prefix='/docs')

with app.app_context():
    try:
        db.engine.connect()
        print("Connected to the database")
    except Exception as e:
        print("Failed to connect to the database:", str(e))

if __name__ == '__main__':
    # Check if connected to the database
    app.run(debug=True)
