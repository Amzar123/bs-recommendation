from flask_sqlalchemy import SQLAlchemy

db_model = SQLAlchemy()
class Student:
    __tablename__ = 'students'

    id = db_model.Column(db_model.String, primary_key=True)
    name = db_model.Column(db_model.String(50))
    email = db_model.Column(db_model.String(50))
    password = db_model.Column(db_model.String(50))
    institution = db_model.Column(db_model.String(50))
    code = db_model.Column(db_model.String(50))
    created_at = db_model.Column(db_model.DateTime)
    updated_at = db_model.Column(db_model.DateTime)

    def __init__(
            self,
            name,
            email,
            password,
            code,
            institution,
            created_at,
            updated_at):
        self.name = name
        self.email = email
        self.password = password
        self.institution = institution
        self.code = code
        self.created_at = created_at
        self.updated_at = updated_at
