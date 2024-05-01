from utils.util import Util


class Answer(Util.get_db().Model):
    __tablename__ = 'answers'

    id = Util.get_db().Column(Util.get_db().Integer, primary_key=True)
    answer = Util.get_db().Column(Util.get_db().String(50))
    assesment_id = Util.get_db().Column(
        Util.get_db().Integer,
        Util.get_db().ForeignKey('assesment.id'))
    is_correct = Util.get_db().Column(Util.get_db().Boolean)
    created_at = Util.get_db().Column(Util.get_db().DateTime)
    updated_at = Util.get_db().Column(Util.get_db().DateTime)

    def __init__(
            self,
            answer,
            assesment_id,
            is_correct,
            created_at,
            updated_at):
        self.answer = answer
        self.assesment_id = assesment_id
        self.is_correct = is_correct
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def get_all_answers():
        return Answer.query.all()
