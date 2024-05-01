from utils.util import Util


class Assesment(Util.get_db().Model):
    __tablename__ = 'assesments'

    id = Util.get_db().Column(Util.get_db().Integer, primary_key=True)
    title = Util.get_db().Column(Util.get_db().String(50))
    description = Util.get_db().Column(Util.get_db().String(50))
    teacher_id = Util.get_db().Column(
        Util.get_db().Integer,
        Util.get_db().ForeignKey('teachers.id'))
    student_id = Util.get_db().Column(
        Util.get_db().Integer,
        Util.get_db().ForeignKey('students.id'))
    created_at = Util.get_db().Column(Util.get_db().DateTime)
    updated_at = Util.get_db().Column(Util.get_db().DateTime)

    def __init__(
            self,
            title,
            description,
            teacher_id,
            student_id,
            created_at,
            updated_at):
        self.title = title
        self.description = description
        self.teacher_id = teacher_id
        self.student_id = student_id
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def get_all_assesments():
        return Assesment.query.all()
