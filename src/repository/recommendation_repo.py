"""
Author: Aji Muhammad Zapar
Date: 2024-05-01
"""

from sqlalchemy.orm import sessionmaker
from src.model.recommendation import Recommendation
from sqlalchemy import text

class RecommendationRepo:
    """
    This class represents the recommendation repository.
    """

    def __init__(self, db):
        self.db = db

    def get_recommendations(self, ids: list):
        """
        This is function to get recommendations by query
        """
        print("ini dia self nya ", self.db)
        # Make query to table recommendations based on the ids
 
        # results = self.db.execute(query, ids=ids)
        
        query = text('SELECT * FROM recommendations WHERE student_id = ANY(:ids)')
        result = self.db.session.execute(query, {'ids': ids}).fetchall()
        return result
