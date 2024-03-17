
class RecommendationService:
    def __init__(self, recommendation_repository):
        self.recommendation_repository = recommendation_repository

    def get_recommendations(self):
        return self.recommendation_repository.get_recommendations()