from src.repository.recommendation_repo import RecommendationRepo
class RecommendationService:
    def __init__(self, recommendation_repository: RecommendationRepo):
        self.recommendation_repository = recommendation_repository

    def get_recommendations(self):
        return self.recommendation_repository.get_recommendations()