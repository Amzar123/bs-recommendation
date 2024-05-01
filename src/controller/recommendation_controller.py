
"""
Author: Aji Muhammad Zapar
Date: 2024-05-01
"""
from flask import Blueprint, jsonify
from src.service.recommendation_service import RecommendationService
from src.utils.response import Response


class RecommendationController:
    """
    This class represents the recommendation controller.

    It provides methods to handle recommendation-related operations.
    """

    def __init__(self, recommendation_service: RecommendationService):
        """
        Initializes a new instance of the RecommendationController class.

        Args:
          recommendation_service (RecommendationService): An instance of RecommendationService.

        Returns:
          None
        """
        self.recommendation_service = recommendation_service
        self.blueprint = Blueprint('controller_blueprint', __name__)

        self.blueprint.add_url_rule(
            '/list',
            view_func=self.get_recommendations,
            methods=['GET']
        )

    def get_recommendations(self):
        """
        Get recommendation by IDs.

        Returns:
          A list of recommendations.

        Raises:
          404: If recommendation is not found.
        """
        result = self.recommendation_service.get_recommendations()
        return Response(
            message='Recommendations retrieved successfully',
            data={
                "doc": result,
            },
            code=200
        ).to_dict()
