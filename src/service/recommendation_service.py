"""
Import required dependencies
"""
from src.repository.recommendation_repo import RecommendationRepo


class RecommendationService:
    """
    This class is for serve recommendation
    """
    def __init__(self, recommendation_repo: RecommendationRepo):
        self.recommendation_repo = recommendation_repo

    def get_recommendations(self, ids: list):
        """
        Function to handle get recommendation
        """
        result = self.recommendation_repo.get_recommendations(ids)
        return result
