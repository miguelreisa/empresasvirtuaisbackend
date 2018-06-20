
from db import db
import random

#https://www.cyberciti.biz/python-tutorials/securely-hash-passwords-in-python/
class ServiceProviderModel(db.Model):

    __tablename__ = 'serviceproviders'

    id = db.Column(db.Integer, primary_key = True)
    enterpriseName = db.Column(db.String(255))
    serviceType = db.Column(db.String(255))
    description = db.Column(db.String(1000))
    localization = db.Column(db.String(255))
    rating = db.Column(db.Float(precision=2))

    userId = db.Column(db.String(255), db.ForeignKey('users.userId'))

    def __init__(self, enterpriseName, serviceType, description, user_id,localization):
        self.enterpriseName = enterpriseName
        self.serviceType = serviceType
        self.description = description
        self.userId = user_id
        self.localization = localization
        self.rating = round(random.uniform(2,5), 2)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            'id' : self.id,
            'userId' : self.userId,
            'enterpriseName' : self.enterpriseName,
            'serviceType' : self.serviceType,
            'description' : self.description,
            'localization' : self.localization,
            'rating' : self.rating
        }


    @classmethod #visto que nao usamos o self
    def find_by_username(cls, username):
        return cls.query.filter_by(userId=username).first()

    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(enterpriseName=name).first()

    @classmethod
    def find_by_serviceType(cls, serviceType):
        return cls.query.filter_by(serviceType=serviceType).all()

    @classmethod
    def find_by_filters(cls, enterpriseName, serviceType, localization):
        if enterpriseName != "":
            if serviceType != "":
                if localization != "":
                    return cls.query.filter_by(enterpriseName=enterpriseName, serviceType=serviceType, localization=localization).all()
                else:
                    return cls.query.filter_by(enterpriseName=enterpriseName, serviceType=serviceType).all()
            else:
                if localization != "":
                    return cls.query.filter_by(enterpriseName=enterpriseName, localization=localization).all()
                else:
                    return cls.query.filter_by(enterpriseName=enterpriseName).all()
        else:
            if serviceType != "":
                if localization != "":
                    return cls.query.filter_by(serviceType=serviceType, localization=localization).all()
                else:
                    return cls.query.filter_by(serviceType=serviceType).all()
            else:
                if localization != "":
                    return cls.query.filter_by(localization=localization).all()
                else:
                    return cls.query.all()
        

        return cls.query.all()
