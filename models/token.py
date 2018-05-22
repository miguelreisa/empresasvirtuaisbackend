from db import db
import time
import uuid

class TokenModel(db.Model):

    __tablename__ = 'Tokens'

    userId = db.Column(db.String(255), primary_key = True)
    tokenId = db.Column(db.String(255))
    creationData = db.Column(db.Integer)
    expirationData = db.Column(db.Integer)

    current_milli_time = lambda: int(round(time.time() * 1000))

    expiration_time = 30000

    def __init__(self,userId):
        self.userId = userId
        self.tokenId = uuid.uuid4().hex #seguro para tokens se for versao 4
        self.creationData = TokenModel.current_milli_time()
        self.expirationData = self.creationData + TokenModel.expiration_time

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def updateToken(self):
        self.tokenId = uuid.uuid4().hex

    @classmethod
    def find_by_username(cls,username):
        return cls.query.filter_by(userId=username).first()
