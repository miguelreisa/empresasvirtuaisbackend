import sqlite3
from flask_restful import Resource, reqparse
from models.event import EventModel
from models.user import UserModel
from models.token import TokenModel
from models.partnership import PartnershipModel
#from models.salt import SaltModel
from passlib.hash import pbkdf2_sha256
import uuid

class EventList(Resource):


    parser = reqparse.RequestParser()
    parser.add_argument('eventName',
        type = str,
        required = False,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('eventType',
        type = str,
        required = False,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('localization',
        type = str,
        required = False,
        help = "This field cannot be left blank!"
    )

    def post(self):
        data = EventList.parser.parse_args()
        eventName = data['eventName']
        eventType = data['eventType']
        eventLocalization = data['localization']

        try:
            return {'events' : [event.json() for event in EventModel.find_by_filters(eventName, eventType, eventLocalization)]}
        except:
            return {"message":"An error occurred, if this continues please contact us."}, 500


    def get(self):
        return {'events' : [event.json() for event in EventModel.query.all()] } #devolve todos os objectos na db
