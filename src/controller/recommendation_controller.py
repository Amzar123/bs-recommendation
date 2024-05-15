
"""
Author: Aji Muhammad Zapar
Date: 2024-05-01
"""
from flask import Blueprint, request
from src.service.recommendation_service import RecommendationService
from src.utils.response import Response

from src.middleware.auth import authenticate_token


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
            methods=['POST']
        )

        self.blueprint.add_url_rule(
            '/question/upload',
            view_func=self.upload_questions,
            methods=['POST']
        )

        self.blueprint.add_url_rule(
            '/generate',
            view_func=self.generate_recommendation,
            methods=['POST']
        )

    @authenticate_token
    def upload_questions(self):
        """
        Upload questions to the recommendation system.
        ---
        parameters:
         - name: body
           in: body
           required: true
           schema:
            type: object
            properties:
              questions:
               type: array
               items:
                type: object
                properties:
                 id:
                  type: string
                  description: The ID of the question
                 text:
                  type: string
                  description: The text of the question
            required: questions
           description: Array of questions
        responses:
         200:
          description: Questions uploaded successfully
          schema:
            type: object
            properties:
             code:
              type: integer
             message:
              type: string
             status:
              type: string
        Returns:
          A success message.
        """
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return Response(
                message='Invalid request content type',
                code=400
            ).to_dict()

        if not request.is_json:
            return Response(
                message='Request body must be a valid JSON object',
                code=400
            ).to_dict()

        request_body = request.get_json()
        if 'questions' not in request_body:
            return Response(
                message='Request body must contain a "questions" field',
                code=400
            ).to_dict()

        questions = request_body['questions']

        self.recommendation_service.upload_questions(questions)

        return Response(
            message='Questions uploaded successfully',
            code=200
        ).to_dict()
    
    @authenticate_token
    def generate_recommendation(self):
        """
        Generate recommendations 
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
            description: Array of student IDs
        responses:
          200:
            description: Recommendation generated successfully
            schema:
              type: object
              properties:
              code:
                type: integer
              message:
                type: string
              status:
                type: string
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
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return Response(
                message='Invalid request content type',
                code=400
            ).to_dict()

        if not request.is_json:
            return Response(
                message='Request body must be a valid JSON object',
                code=400
            ).to_dict()

        request_body = request.get_json()
        if 'ids' not in request_body:
            return Response(
                message='Request body must contain a "ids" field',
                code=400
            ).to_dict()

        ids = request_body['ids']

        res = self.recommendation_service.generate_recommendations(ids)

        return Response(
            message='Recommendation generated successfully',
            data=res,
            code=200
        ).to_dict()

    @authenticate_token
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
        Returns:
          A list of recommendations.
        Raises:
          404: If recommendation is not found.
        """
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return Response(
                message='Invalid request content type',
                code=400
            ).to_dict()

        if not request.is_json:
            return Response(
                message='Request body must be a valid JSON object',
                code=400
            ).to_dict()

        request_body = request.get_json()
        if 'ids' not in request_body:
            return Response(
                message='Request body must contain an "ids" field',
                code=400
            ).to_dict()

        ids = request_body['ids']

        result = self.recommendation_service.get_recommendations(ids)
        return Response(
            message='Recommendations retrieved successfully',
            data={
                "doc": result,
            },
            code=200
        ).to_dict()
