from utils.util import Util

class Recommendation(Util.get_db().Model):
    __tablename__ = 'recommendations'

    id = Util.get_db().Column(Util.get_db().Integer, primary_key=True)
    recommendation = Util.get_db().Column(Util.get_db().String(50))
    created_at = Util.get_db().Column(Util.get_db().DateTime)
    updated_at = Util.get_db().Column(Util.get_db().DateTime)

    def __init__(self, recommendation, created_at, updated_at):
        self.recommendation = recommendation
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def get_all_recommendations():
        return Recommendation.query.all()