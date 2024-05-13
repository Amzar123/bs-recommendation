"""
Author: Aji Muhammad Zapar
Date: 2024-05-01
"""
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
        query = text(
            'SELECT * FROM recommendations WHERE student_id = ANY(:ids)')
        result = self.db.session.execute(query, {'ids': ids}).fetchall()
        return self.row_to_dict(result)

    def row_to_dict(self, rows):
        """
        Convert a list of Row objects to a list of dictionaries.
        """
        if rows is None:
            return None
        return [dict(row._asdict()) for row in rows]
