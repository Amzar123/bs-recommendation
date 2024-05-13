"""
Import required dependencies
"""
from src.repository.recommendation_repo import RecommendationRepo
from src.repository.student_repository import StudentRepo


class RecommendationService:
    """
    This class is for serve recommendation
    """

    def __init__(
            self,
            recommendation_repo: RecommendationRepo,
            student_repo: StudentRepo):
        self.recommendation_repo = recommendation_repo
        self.student_repo = student_repo

    def __apriori(self):
        return "to be implemented"

    def __fpgrowth(self):
        return "to be implemented"

    def get_recommendations(self, ids: list):
        """
        Function to handle get recommendation
        """
        result = self.recommendation_repo.get_recommendations(ids)
        return result

    def generate_recommendations(self, ids: list):
        """
        Function to handle generate recommendation
        """
        # get student by ids
        students = self.student_repo.get_student_by_ids(ids)

        # generate item set with apriori
        itemsets = self.__apriori()

        # generate item set with fpgrowth
        items = self.__fpgrowth()

        print(items, itemsets)

        return students
    