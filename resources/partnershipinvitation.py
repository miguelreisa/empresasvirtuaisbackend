import sqlite3
from flask_restful import Resource, reqparse
from models.event import EventModel
from models.user import UserModel
from models.token import TokenModel
from models.partnership import PartnershipModel
from models.serviceprovider import ServiceProviderModel
#from models.salt import SaltModel
from passlib.hash import pbkdf2_sha256
import uuid

class InvitationAcceptance(Resource):


    parser = reqparse.RequestParser()
    parser.add_argument('userId',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('tokenId',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('partnershipId',
        type = int,
        required = True,
        help = "This field cannot be left blank!"
    )


    def post(self):
        data = InvitationAcceptance.parser.parse_args()
        print("AA")

        try:
            user = UserModel.find_by_username(data['userId'])
            partnership = PartnershipModel.find_by_id(data['partnershipId'])
            print("BB")
            if user:

                if not partnership:
                    return{'message' : "Partnership offer given does not exist!"}, 400
                if user.userType != "provider":
                    return {'message' : "You need to be a provider to accept partnerships offers!"}, 403

                serviceprovider = ServiceProviderModel.find_by_username(data['userId'])


                print("CC")
                userToken = TokenModel.find_by_username(data['userId'])
                if userToken:
                    if userToken.tokenId == data['tokenId']:
                        print("DD")
                        partnership = PartnershipModel.find_by_id(data['partnershipId'])
                        print("EE")
                        if not partnership:
                            return {"message" : "This partnership offer was not found."}, 400
                        if partnership.serviceProviderId != serviceprovider.id:
                            return {"message" : "You are not the provider of this partnership offer."}, 400

                        if partnership.accepted == 1:
                            return {"message" : "You already accepted this partnership offer!"}, 400

                        print("FF")

                        partnership.accepted = 1
                        partnership.save_to_db()

                        return {'message' : 'Partnership invitation accepted! You can know start working with the organizer of the event.'}, 201

        except:
            return {"message":"An error occurred, if this continues please contact us."}, 500


        return {'message' : 'Invalid input.'}, 403

class InvitationReject(Resource):


    parser = reqparse.RequestParser()
    parser.add_argument('userId',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('tokenId',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('partnershipId',
        type = int,
        required = True,
        help = "This field cannot be left blank!"
    )


    def post(self):
        data = InvitationReject.parser.parse_args()
        print("AA")

        try:
            user = UserModel.find_by_username(data['userId'])
            partnership = PartnershipModel.find_by_id(data['partnershipId'])
            print("BB")
            if user:

                if not partnership:
                    return{'message' : "Partnership offer given does not exist!"}, 400
                if user.userType != "provider":
                    return {'message' : "You need to be a provider to reject partnerships offers!"}, 403

                serviceprovider = ServiceProviderModel.find_by_username(data['userId'])


                print("CC")
                userToken = TokenModel.find_by_username(data['userId'])
                if userToken:
                    if userToken.tokenId == data['tokenId']:
                        print("DD")
                        partnership = PartnershipModel.find_by_id(data['partnershipId'])
                        print("EE")
                        if not partnership:
                            return {"message" : "This partnership offer was not found."}, 400
                        if partnership.serviceProviderId != serviceprovider.id:
                            return {"message" : "You are not the provider of this partnership offer."}, 400

                        if partnership.accepted == 0:
                            return {"message" : "You already accepted this partnership offer!"}, 400

                        print("FF")

                        partnership.accepted = 0
                        partnership.serviceProviderId = -1
                        partnership.serviceProviderName = "none"
                        partnership.save_to_db()

                        return {'message' : 'Partnership invitation rejected.'}, 201

        except:
            return {"message":"An error occurred, if this continues please contact us."}, 500


        return {'message' : 'Invalid input.'}, 403



class PartnershipInvitation(Resource):


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
    parser.add_argument('providerId',
        type = int,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('eventId',
        type = int,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('serviceType',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    

    def post(self):
        data = PartnershipInvitation.parser.parse_args()
        print("AA")

        try:
            user = UserModel.find_by_username(data['organizerId'])
            event = EventModel.find_by_id(data['eventId'])
            print("BB")
            if user:

                if not event:
                    return{'message' : "Event given does not exist!"}, 400
                if user.userType != "organizer" or event.organizerId != data['organizerId'] :
                    return {'message' : "You need to be the organizer of this event!"}, 403

                print("CC")
                userToken = TokenModel.find_by_username(data['organizerId'])
                if userToken:
                    if userToken.tokenId == data['tokenId']:
                        print("DD")
                        partnership = PartnershipModel.find_by_eventIdAndServiceType(data['eventId'], data['serviceType'])
                        print("EE")
                        if not partnership:
                            return {"message" : "This type of partnership was not found for this event."}, 400
                        if partnership.serviceProviderId != -1:
                            return {"message" : "A provider was already invited or has accepted for this service type."}, 400

                        print("FF")
                        provider = ServiceProviderModel.find_by_id(data['providerId'])
                        if not provider:
                            return {"message" : "Provider given was not found."}, 400

                        if provider.serviceType != data['serviceType']:
                            return {"message" : "Provider selected does not offer this type of service."}

                        print("GG")
                        partnership.serviceProviderId = data['providerId']
                        partnership.serviceProviderName = provider.enterpriseName
                        partnership.save_to_db()

                        return {'message' : 'Partnership invitation created! Wait for the response of the service provider.'}, 201

        except:
            return {"message":"An error occurred, if this continues please contact us."}, 500


        return {'message' : 'Invalid input.'}, 403
