from src.utils.util import Util


# class Teacher(Util.get_db().Model):
#     __tablename__ = 'teachers'

#     id = Util.get_db().Column(Util.get_db().Integer, primary_key=True)
#     name = Util.get_db().Column(Util.get_db().String(50))
#     email = Util.get_db().Column(Util.get_db().String(50))
#     password = Util.get_db().Column(Util.get_db().String(50))
#     code = Util.get_db().Column(Util.get_db().String(50))
#     created_at = Util.get_db().Column(Util.get_db().DateTime)
#     updated_at = Util.get_db().Column(Util.get_db().DateTime)

#     def __init__(
#             self,
#             name,
#             email,
#             password,
#             code,
#             institution,
#             created_at,
#             updated_at):
#         self.name = name
#         self.email = email
#         self.password = password
#         self.code = code
#         self.created_at = created_at
#         self.updated_at = updated_at

#     @staticmethod
#     def get_all_teachers():
#         return Teacher.query.all()
