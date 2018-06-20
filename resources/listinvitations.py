import sqlite3
from flask_restful import Resource, reqparse
from models.event import EventModel
from models.user import UserModel
from models.token import TokenModel
from models.partnership import PartnershipModel
#from models.salt import SaltModel
from passlib.hash import pbkdf2_sha256
import uuid

class ListInvitations(Resource):

    def get(self,providerId):
        return {'invitations' : [partnership.json() for partnership in PartnershipModel.find_by_serviceProviderId(providerId)] } #devolve todos os objectos na db
