
import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from models.token import TokenModel
#from models.salt import SaltModel
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

                return {'userId' : data['username'], 'tokenId' : userToken.tokenId}, 200

        return {'message' : 'Invalid input.'}, 403



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
    parser.add_argument('firstName',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('lastName',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('country',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('localizationName',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )



    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message" : "User with that username already exists."}, 400

        user = UserModel(**data)
        user.save_to_db()

        #not saving salts
        #salt = SaltModel(data['username'])
        #salt.save_to_db()


        return {"message" : "User Created Successfully"}
