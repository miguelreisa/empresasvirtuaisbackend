import sqlite3
from flask_restful import Resource, reqparse
from models.event import EventModel
from models.user import UserModel
from models.token import TokenModel
from models.serviceprovider import ServiceProviderModel
#from models.salt import SaltModel
from passlib.hash import pbkdf2_sha256
import uuid

class ProviderList(Resource):


    parser = reqparse.RequestParser()
    parser.add_argument('providerName',
        type = str,
        required = False,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('serviceType',
        type = str,
        required = False,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('serviceLocalization',
        type = str,
        required = False,
        help = "This field cannot be left blank!"
    )

    def post(self):
        data = ProviderList.parser.parse_args()
        providerName = data['providerName']
        serviceType = data['serviceType']
        serviceLocalization = data['serviceLocalization']

        try:
            return {'providers' : [provider.json() for provider in ServiceProviderModel.find_by_filters(providerName, serviceType, serviceLocalization)]}
        except:
            return {"message":"An error occurred, if this continues please contact us."}, 500


    def get(self):
        return {'service_providers' : [provider.json() for provider in ServiceProviderModel.query.all()] } #devolve todos os objectos na db
