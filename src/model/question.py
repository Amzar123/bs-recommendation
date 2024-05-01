from src.utils.util import Util



class Question(Util.get_db().Model):
    __tablename__ = 'questions'

    id = Util.get_db().Column(Util.get_db().Integer, primary_key=True)
    question = Util.get_db().Column(Util.get_db().String(50))
    key_answer = Util.get_db().Column(Util.get_db().String(50))
    created_at = Util.get_db().Column(Util.get_db().DateTime)
    updated_at = Util.get_db().Column(Util.get_db().DateTime)

    def __init__(self, title, description, created_at, updated_at):
        self.title = title
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def get_all_questions():
        return Question.query.all()
