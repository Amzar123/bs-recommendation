from flask import Blueprint, jsonify
from src.service.recommendation_service import RecommendationService

class RecommendationController:
    def __init__(self, recommendation_service: RecommendationService):
        self.recommendation_service = recommendation_service
        self.blueprint = Blueprint('controller_blueprint', __name__)

        self.blueprint.add_url_rule(
            '/get',
            view_func=self.get_recommendations,
            methods=['GET']
        )

    def get_recommendations(self):
        return self.recommendation_service.get_recommendations()