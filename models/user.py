
from db import db
from passlib.hash import pbkdf2_sha256
from models.organizer import OrganizerModel
from models.serviceprovider import ServiceProviderModel

#https://www.cyberciti.biz/python-tutorials/securely-hash-passwords-in-python/
class UserModel(db.Model):

    __tablename__ = 'users'

    userId = db.Column(db.String(255), primary_key = True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))
    name = db.Column(db.String(255))
    localization = db.Column(db.String(255))
    userType = db.Column(db.String(255)) #normal, organizer or provider

    organizer = db.relationship('OrganizerModel', lazy='dynamic')
    service_provider = db.relationship('ServiceProviderModel', lazy='dynamic')

    def __init__(self, username, password, email, name, localization, userType):
        self.userId = username
        self.password = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
        self.email = email
        self.name = name
        self.localization = localization
        self.userType = userType

    def json(self):
        return {
            'userId' : self.userId,
            'email' : self.email,
            'name' : self.name,
            'localization' : self.localization,
            'userType' : self.userType
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def check_password(self,password):
        return pbkdf2_sha256.verify(password, self.password)

    def change_password(self, newPassword):
        self.password = pbkdf2_sha256.encrypt(newPassword, rounds=200000, salt_size=16)
        db.session.add(self)
        db.session.commit()

    @classmethod #visto que nao usamos o self
    def find_by_username(cls, username):
        return cls.query.filter_by(userId=username).first()
