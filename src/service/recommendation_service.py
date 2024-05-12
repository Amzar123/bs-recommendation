from src.service.mapper.recommendation import RecommendationMapper
from src.repository.recommendation_repo import RecommendationRepo


class RecommendationService:
    def __init__(self, recommendation_repo: RecommendationRepo):
        self.recommendation_repo = recommendation_repo

    def get_recommendations(self, ids: list):
        result = self.recommendation_repo.get_recommendations(ids)
        # mapped = RecommendationMapper.map_recommendation(recommendation_data=result)
        # return  mapped # Fix: Pass 'result' as an argument to 'map_recommendation' method.
        return result
