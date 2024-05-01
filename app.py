"""
This is the server file that runs the application.

Author: Aji Muhammad Zapar
Date: 2024-05-01
"""

from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from src.controller.recommendation_controller import RecommendationController
from src.repository.recommendation_repo import RecommendationRepo
from src.service.recommendation_service import RecommendationService
from src.utils.util import Util

app = Flask(__name__)



db = Util.get_db(app)

# Perform database migration
migrate = Migrate(app, db)

# Register the blueprint from the repository
recommendation_repository = RecommendationRepo(db)

# Register the blueprint from the service
recommendation_service = RecommendationService(recommendation_repository)

@app.route("/spec")
def spec():
    """
    this is route for api spec on swagger
    """
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Recommendation System API"
    return jsonify(swag)


# Route to serve Swagger UI
swaggerui_blueprint = get_swaggerui_blueprint('/docs', '/spec')
app.register_blueprint(swaggerui_blueprint, url_prefix='/docs')

# Register the blueprint from the controller
recommendation_controller = RecommendationController(recommendation_service)
app.register_blueprint(
    recommendation_controller.blueprint,
    url_prefix='/recommendations'
)

with app.app_context():
    try:
        db.engine.connect()
        print("Connected to the database")
    except Exception as e:
        print("Failed to connect to the database:", str(e))

if __name__ == '__main__':
    # Check if connected to the database
    app.run(debug=True)
