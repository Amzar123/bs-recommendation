from flask import Flask, jsonify
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from src.controller.recommendation_controller import RecommendationController
from src.repository.recommendation_repo import RecommendationRepo
from src.service.recommendation_service import RecommendationService
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

@app.route('/my-resource/<int:id>')
def get_resource(id):
    """
    This is a sample endpoint that fetches a resource by ID.
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the resource
    responses:
      200:
        description: A single resource
        schema:
          id: Resource
          properties:
            id:
              type: integer
              description: The ID of the resource
            name:
              type: string
              description: The name of the resource
    """
    # Your implementation to fetch the resource
    return {'id': id, 'name': 'Sample Resource'}, 200

@app.route("/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "My API"
    return jsonify(swag)

# Konfigurasi koneksi database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/database_name'
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

# Route to serve Swagger UI
swaggerui_blueprint = get_swaggerui_blueprint('/docs', '/spec')
app.register_blueprint(swaggerui_blueprint, url_prefix='/docs')

if __name__ == '__main__':
    app.run(debug=True)