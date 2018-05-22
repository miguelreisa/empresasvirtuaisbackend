'''from db import db
import random
import string


#https://stackoverflow.com/questions/36057308/bcrypt-how-to-store-salt-with-python3#36060391
#nao e preciso guardar salt com bcrypt mas estamos a guardar para aprendizagem
class SaltModel(db.Model):

    __tablename__ = 'Salts'

    userId = db.Column(db.String(255), primary_key = True)
    salt = db.Column(db.String(255))

    def __init__(self, userId):
        self.userId = userId
        self.salt = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(20)]) #gerar salt
        print(self.salt)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod #visto que nao usamos o self
    def find_by_username(cls, username):
        return cls.query.filter_by(userId=username).first()
'''
