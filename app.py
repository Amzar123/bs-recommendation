from flask import Flask, jsonify
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from src.controller.recommendation_controller import RecommendationController
from src.repository.recommendation_repo import RecommendationRepo
from src.service.recommendation_service import RecommendationService
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Construct the database connection URL
# DB_USERNAME = os.getenv("DATABASE_USER")
# DB_NAME = os.getenv("DATABASE_NAME")
# DB_HOST = os.getenv("DATABASE_HOST")
# DB_PORT = os.getenv("DATABASE_PORT")
# DB_PASSWORD = os.getenv("DATABASE_PASSWORD")

# # logging db port 
# print(DB_PORT)

DB_URL = f"postgresql://postgres:postgres@localhost:5432/recommendations"

# Konfigurasi koneksi database
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import db 
db = SQLAlchemy(app)

# Register the blueprint from the repository
recommendation_repository = RecommendationRepo(db)

# Register the blueprint from the service 
recommendation_service = RecommendationService(recommendation_repository)

# Register the blueprint from the controller
recommendation_controller = RecommendationController(recommendation_service)
app.register_blueprint(recommendation_controller.blueprint, url_prefix='/recommendations')

@app.route("/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Recommendation System API"
    return jsonify(swag)

# Route to serve Swagger UI
swaggerui_blueprint = get_swaggerui_blueprint('/docs', '/spec')
app.register_blueprint(swaggerui_blueprint, url_prefix='/docs')

if __name__ == '__main__':
    app.run(debug=True)