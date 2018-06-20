
from db import db

class PartnershipModel(db.Model):

    __tablename__ = 'partnerships'

    id = db.Column(db.Integer, primary_key = True)
    serviceType = db.Column(db.String(255))
    needed = db.Column(db.Integer)
    serviceProviderId = db.Column(db.Integer)
    serviceProviderName = db.Column(db.String(255))
    price = db.Column(db.Integer)
    accepted = db.Column(db.Integer)
    description = db.Column(db.String(1000))

    eventId = db.Column(db.Integer, db.ForeignKey('events.id'))
    eventName = db.Column(db.String(255))

    def __init__(self,serviceType,needed,eventId,eventName):
        s = 1
        self.serviceType = serviceType
        self.needed = needed #0 if not needed, 1 if needed
        self.eventId = eventId
        self.eventName = eventName
        self.serviceProviderId = -1 #if -1 there is no partnership for this serviceType yet
        self.serviceProviderName = "none" #if 'none' there is no partnership for this serviceType yet
        self.price = -1 #if -1 there is no partnership for this serviceType yet
        self.accepted = 0 #0 if not accepted, 1 if accepted
        self.description = ""

    def json(self):
        return {
            'id' : self.id,
            'serviceType' : self.serviceType,
            'needed' : self.needed,
            'eventId' : self.eventId,
            'eventName' : self.eventName,
            'serviceProviderId' : self.serviceProviderId,
            'serviceProviderName' : self.serviceProviderName,
            'price' : self.price,
            'accepted' : self.accepted,
            'description' : self.description
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod #visto que nao usamos o self
    def find_by_eventId(cls, eventId):
        return cls.query.filter_by(eventId=eventId).all()

    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()


    @classmethod
    def find_by_serviceType(cls, serviceType):
        return cls.query.filter_by(serviceType=serviceType).all()

    @classmethod
    def find_by_eventIdAndServiceType(cls, eventId, serviceType):
        return cls.query.filter_by(eventId=eventId,serviceType=serviceType).first()

    @classmethod
    def find_by_serviceProviderId(cls, providerId):
        return cls.query.filter_by(serviceProviderId=providerId).all()
