
from db import db
from passlib.hash import pbkdf2_sha256
#https://www.cyberciti.biz/python-tutorials/securely-hash-passwords-in-python/
class OrganizerModel(db.Model):

    __tablename__ = 'organizers'

    id = db.Column(db.Integer, primary_key = True)
    enterpriseName = db.Column(db.String(255))
    description = db.Column(db.String(1000))

    userId = db.Column(db.String(255), db.ForeignKey('users.userId'))

    def __init__(self, enterpriseName, description, user_id):
        self.enterpriseName = enterpriseName
        self.description = description
        self.userId = user_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            'id' : self.id,
            'userId' : self.userId,
            'enterpriseName' : self.enterpriseName,
            'description' : self.description
        }


    @classmethod #visto que nao usamos o self
    def find_by_name(cls, name):
        return cls.query.filter_by(enterpriseName=name).first()

    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_username(cls,userId):
        return cls.query.filter_by(userId=userId).first()
