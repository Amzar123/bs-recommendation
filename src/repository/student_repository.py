from sqlalchemy import text


class StudentRepo:
    """
    This class represents the recommendation repository.
    """

    def __init__(self, db):
        self.db = db

    def get_student_by_email(self, email, password):
        """
        This is function to get student by query
        """
        query = text(
            'SELECT * FROM students WHERE email = :email AND password = :password')
        result = self.db.session.execute(
            query, {'email': email, 'password': password}).fetchone()
        return self.row_to_dict(result)
    
    def get_student_by_ids(self, ids):
        """
        This is function to get student by query 
        """
        query = text(
            'SELECT * FROM students WHERE id = ANY(:ids)')
        result = self.db.session.execute(query, {'ids': ids}).fetchall()
        return [self.row_to_dict(row) for row in result]

    def row_to_dict(self, row):
        """
        Convert a Row object to a dictionary.
        """
        if row is None:
            return None
        return dict(row._asdict())
