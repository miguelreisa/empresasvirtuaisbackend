from db import db

import time
import uuid
from models.partnership import PartnershipModel

class EventModel(db.Model):

    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key = True)
    organizerId = db.Column(db.String(255))
    eventName = db.Column(db.String(255))
    eventType = db.Column(db.String(255))
    dateInterval = db.Column(db.String(255))
    localization = db.Column(db.String(255))
    description = db.Column(db.String(1000))

    partnerships = db.relationship('PartnershipModel', lazy='dynamic')

    def __init__(self, organizerId, eventName, eventType, dateInterval, localization, description):
        self.organizerId = organizerId
        self.eventName = eventName
        self.eventType = eventType
        self.dateInterval = dateInterval
        self.localization = localization
        self.description = description


    def json(self):
        return {
            'id' : self.id,
            'organizerId' : self.organizerId,
            'eventName' : self.eventName,
            'eventType' : self.eventType,
            'dateInterval' : self.dateInterval,
            'localization' : self.localization,
            'description' : self.description,
            'partnerships' : [partnership.json() for partnership in self.partnerships.all()]
        } #qd usamos lazy='dynamic', o self.papersOuPCmembers ja nao e lista de items mas sim um query builder

    def getScheduledEvents(self):
        return self.scheduledevents.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod #visto que nao usamos o self
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(eventName=name).first()

    @classmethod
    def find_by_organizerId(cls, organizerId):
        return cls.query.filter_by(organizerId=organizerId).all()

    @classmethod
    def find_by_eventType(cls, eventType):
        return cls.query.filter_by(eventType=eventType).all()
    
    @classmethod
    def find_by_filters(cls, eventName, eventType, localization):
        if eventName != "":
            if eventType != "":
                if localization != "":
                    return cls.query.filter_by(eventName=eventName, eventType=eventType, localization=localization).all()
                else:
                    return cls.query.filter_by(eventName=eventName, eventType=eventType).all()
            else:
                if localization != "":
                    return cls.query.filter_by(eventName=eventName, localization=localization).all()
                else:
                    return cls.query.filter_by(eventName=eventName).all()
        else:
            if eventType != "":
                if localization != "":
                    return cls.query.filter_by(eventType=eventType, localization=localization).all()
                else:
                    return cls.query.filter_by(eventType=eventType).all()
            else:
                if localization != "":
                    return cls.query.filter_by(localization=localization).all()
                else:
                    return cls.query.all()
        

        return cls.query.all()
