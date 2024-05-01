from utils.util import Util


class Option(Util.get_db().Model):
    __tablename__ = 'options'

    id = Util.get_db().Column(Util.get_db().Integer, primary_key=True)
    option = Util.get_db().Column(Util.get_db().String(50))
    question_id = Util.get_db().Column(
        Util.get_db().Integer,
        Util.get_db().ForeignKey('questions.id'))
    created_at = Util.get_db().Column(Util.get_db().DateTime)
    updated_at = Util.get_db().Column(Util.get_db().DateTime)

    def __init__(self, option, question_id, created_at, updated_at):
        self.option = option
        self.question_id = question_id
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def get_all_options():
        return Option.query.all()
