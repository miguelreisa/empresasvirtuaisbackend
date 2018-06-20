import sqlite3
from flask_restful import Resource, reqparse
from models.event import EventModel
from models.user import UserModel
from models.token import TokenModel
from models.partnership import PartnershipModel
#from models.salt import SaltModel
from passlib.hash import pbkdf2_sha256
import uuid

class Event(Resource):


    parser = reqparse.RequestParser()
    parser.add_argument('organizerId',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('tokenId',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('eventName',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('eventType',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('dateInterval',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('localization',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('description',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('extraPartnerships',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )

    def post(self):
        data = Event.parser.parse_args()

        try:
            user = UserModel.find_by_username(data['organizerId'])

            if user:
                if user.userType != "organizer":
                    return {'message' : "You need to be an organizer in order to create an event!"}, 403

                userToken = TokenModel.find_by_username(data['organizerId'])
                if userToken:
                    if userToken.tokenId == data['tokenId']:
                        if EventModel.find_by_name(data['eventName']):
                            return {"message" : "Event with that name already exists."}, 400

                        event = EventModel(data['organizerId'], data['eventName'], data['eventType'], data['dateInterval'], data['localization'], data['description'])
                        event.save_to_db()

                        #Needed partnerships, creating already but without partner yet
                        lightsPartner = PartnershipModel("Lights",1,event.id,data['eventName'])
                        lightsPartner.save_to_db()
                        localizationPartner = PartnershipModel("Localization", 1, event.id,data['eventName'])
                        localizationPartner.save_to_db()
                        securityPartner = PartnershipModel("Security", 1, event.id,data['eventName'])
                        securityPartner.save_to_db()
                        sanitationPartner = PartnershipModel("Sanitation", 1, event.id,data['eventName'])
                        sanitationPartner.save_to_db()
                        cateringPartner = PartnershipModel("Catering", 1, event.id,data['eventName'])
                        cateringPartner.save_to_db()
                        ticketsPartner = PartnershipModel("Tickets", 1, event.id,data['eventName'])
                        ticketsPartner.save_to_db()

                        if data['extraPartnerships'] != "none":
                            if "." not in data['extraPartnerships']:
                                extraPartner = PartnershipModel(data['extraPartnerships'], 1, event.id,data['eventName'])
                                extraPartner.save_to_db()
                            else:
                                splitExtraPartnerships = data['extraPartnerships'].split('.')
                                for extraPartnership in splitExtraPartnerships:
                                    extraPartner = PartnershipModel(extraPartnership, 1, event.id,data['eventName'])
                                    extraPartner.save_to_db()


                        return {'message' : 'Event accepted and created! You can now start making partnerships!', 'event' : event.json()}, 201

        except:
            return {"message":"An error occurred, if this continues please contact us."}, 500


        return {'message' : 'Invalid input.'}, 403

    def get(self):
        return {'events' : [event.json() for event in EventModel.query.all()] } #devolve todos os objectos na db
