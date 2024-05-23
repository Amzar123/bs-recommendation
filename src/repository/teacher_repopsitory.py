from sqlalchemy import text


class TeacherRepo:
    """
    This class represents the recommendation repository.
    """

    def __init__(self, db):
        self.db = db

    def get_teacher_by_email(self, email, password):
        """
        This is function to get student by query
        """
        query = text(
            'SELECT * FROM teachers WHERE email = :email AND password = :password')
        result = self.db.session.execute(
            query, {'email': email, 'password': password}).fetchone()
        return self.row_to_dict(result)

    def row_to_dict(self, row):
        """
        Convert a Row object to a dictionary.
        """
        if row is None:
            return None
        return dict(row._asdict())
