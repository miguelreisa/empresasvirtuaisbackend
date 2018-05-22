import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS


from resources.user import UserRegister, UserLogin, UserPassword

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db') #dizer ao sqlalchemy onde encontrar o ficheiro .db (aqui dizemos que esta na root folder do projecto). Nao precisa de ser sqlite, pode ser mysql, etc
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #coiso
app.secret_key = 'engsoftware' 
api = Api(app)

api.add_resource(UserRegister , '/register')
api.add_resource(UserLogin , '/login')
api.add_resource(UserPassword, '/profile/change_password')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
