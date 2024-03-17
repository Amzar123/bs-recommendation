from flask import Blueprint, jsonify
from src.service.recommendation_service import RecommendationService

class RecommendationController:
    def __init__(self, recommendation_service: RecommendationService):
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
        ---
        parameters:
         - name: body
           in: body
           required: true
           schema:
            type: object
            properties:
              ids:
               type: array
               items:
                type: string
            required: ids
           description: Array of recommendation IDs
        responses:
         200:
          description: A list of recommendations
          schema:
            type: object
            properties:
             code:
              type: integer
             message: 
              type: string
             status: 
              type: string
             data:
              type: array
              items:
               type: object
               properties:
                id:
                  type: string
                  description: The ID of the recommendation
                name:
                  type: string
                  description: The name of the recommendation
          x-example:
            code: 200
         404:
          description: Recommendation not found
          schema:
            id: Error
            properties:
               code: 
                type: integer
                description: The error code
               message:
                 type: string
                 description: The error message
        """
        return self.recommendation_service.get_recommendations()