from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recommendation(db.Model):
    __tablename__ = 'recommendations'

    id = db.Column(db.String, primary_key=True)
    recommendation = db.Column(db.String)
    student_id = db.Column(db.String, db.ForeignKey('students.id'))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, recommendation, student_id, created_at, updated_at):
        self.recommendation = recommendation
        self.student_id = student_id
        self.created_at = created_at
        self.updated_at = updated_at
