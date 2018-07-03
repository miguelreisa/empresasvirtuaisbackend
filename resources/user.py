
import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from models.token import TokenModel
#from models.salt import SaltModel
from models.organizer import OrganizerModel
from models.serviceprovider import ServiceProviderModel
from passlib.hash import pbkdf2_sha256
import uuid

##Receives userId,oldPassword,newPassword
class UserPassword(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('tokenId',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('oldPassword',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('newPassword',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )

    def post(self):
        data = UserPassword.parser.parse_args()

        try:
            user = UserModel.find_by_username(data['username'])

            if user:
                userToken = TokenModel.find_by_username(data['username'])
                if userToken:
                    if userToken.tokenId == data['tokenId']:
                        if user.check_password(data['oldPassword']):
                            user.change_password(data['newPassword'])
                            user.save_to_db()
                            return {'message' : 'Password changed!'}, 201
        except:
            return {"message":"An error occurred, if this continues please contact us."}, 500


        return {'message' : 'Invalid input.'}, 403





class UserLogin(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('username',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('password',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )

    def post(self):
        data = UserLogin.parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user:
            if user.check_password(data['password']) :
                userToken = TokenModel.find_by_username(data['username'])
                try:
                    if userToken is None:
                        userToken = TokenModel(data['username']) #ou **request_data
                    else:
                        userToken.tokenId = uuid.uuid4().hex

                    userToken.save_to_db()
                except:
                    return {"message":"An error occurred, if this continues please contact us."}, 500

                isUserProvider = ServiceProviderModel.find_by_username(data['username'])
                isUserOrganizer = OrganizerModel.find_by_username(data['username'])
                if isUserProvider:
                    return {'userId' : data['username'], 'tokenId' : userToken.tokenId, 'userType' : user.userType, 'serviceProviderId' : isUserProvider.id, 'serviceProviderName' : isUserProvider.enterpriseName}, 200
                elif isUserOrganizer:
                    return {'userId' : data['username'], 'tokenId' : userToken.tokenId, 'userType' : user.userType, 'enterpriseId' : isUserOrganizer.id, 'enterpriseName' : isUserOrganizer.enterpriseName}, 200
                else:
                    return {'userId' : data['username'], 'tokenId' : userToken.tokenId, 'userType' : user.userType}, 200

        return {'message' : 'Invalid input.'}, 403


class UserList(Resource):
    def get(self):
        return {'users' : [user.json() for user in UserModel.query.all()] } #devolve todos os objectos na db

class OrganizerList(Resource):
    def get(self):
        return {'organizers' : [organizer.json() for organizer in OrganizerModel.query.all()] } #devolve todos os objectos na db

class ServiceProviderList(Resource):
    def get(self):
        return {'service_providers' : [provider.json() for provider in ServiceProviderModel.query.all()] } #devolve todos os objectos na db

class UserRegister(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('username',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('password',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('email',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('name',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('localization',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('userType',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )

    #PARSER FOR ORGANIZER
    parser2 = reqparse.RequestParser()
    parser2.add_argument('enterpriseName',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser2.add_argument('description',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )

    #PARSER FOR SERVICE serviceProvider
    parser3 = reqparse.RequestParser()
    parser3.add_argument('enterpriseName',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser3.add_argument('serviceType',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser3.add_argument('description',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser3.add_argument('serviceLocalization',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )


    def post(self):
        data = UserRegister.parser.parse_args()
        print(data)
        if UserModel.find_by_username(data['username']):
            return {"message" : "User with that username already exists."}, 400
        
        if len(data['password']) < 8:
            return {"message" : "Your password needs to have atleast 8 characters."}, 400

        if data['userType'] == "normal" or data['userType'] == "organizer" or data['userType'] == "provider":
            if data['userType'] == "organizer":
                data2 = UserRegister.parser2.parse_args()
                print(data2)
                findOrganizer = OrganizerModel.find_by_name(data2['enterpriseName'])
                if findOrganizer:
                    return {"message" : "An organizer with that name already exists!"}, 400
                user = UserModel(data['username'], data['password'], data['email'], data['name'], data['localization'], data['userType'])
                user.save_to_db()
                organizer = OrganizerModel(data2['enterpriseName'], data2['description'], data['username'])
                organizer.save_to_db()
            elif data['userType'] == "provider":
                data3 = UserRegister.parser3.parse_args()
                print(data3)
                findProvider = ServiceProviderModel.find_by_name(data3['enterpriseName'])
                if findProvider:
                    return {"message" : "A provider with that name already exists!"}, 400
                user = UserModel(data['username'], data['password'], data['email'], data['name'], data['localization'], data['userType'])
                user.save_to_db()
                provider = ServiceProviderModel(data3['enterpriseName'], data3['serviceType'], data3['description'], data['username'], data3['serviceLocalization'])
                provider.save_to_db()
            else:
                user = UserModel(data['username'], data['password'], data['email'], data['name'], data['localization'], data['userType'])
                user.save_to_db()
        else:
            return {"message" : "The type of user selected is not available."}, 400


        #not saving salts
        #salt = SaltModel(data['username'])
        #salt.save_to_db()


        return {"message" : "User Created Successfully"}
