import os
from flask import Flask
from flask_restful import Api

from resources.user import UserRegister, UserLogin, UserList, OrganizerList, ServiceProviderList,UserPassword
from resources.event import Event
from resources.eventlist import EventList
from resources.partnershipinvitation import PartnershipInvitation,InvitationAcceptance,InvitationReject
from resources.listinvitations import ListInvitations
from resources.listproviders import ProviderList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'empresasvirtuais'
api = Api(app)


api.add_resource(UserRegister , '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserPassword, '/profile/change_password')
api.add_resource(UserList, '/users')
api.add_resource(OrganizerList, '/organizers')
api.add_resource(ServiceProviderList, '/serviceproviders')
api.add_resource(Event , '/register_event')
api.add_resource(EventList, '/list_events') #has filters
api.add_resource(PartnershipInvitation, '/partnershipinvitation')
api.add_resource(ListInvitations, '/list_invitations/<int:providerId>')
api.add_resource(InvitationAcceptance, '/acceptinvitation')
api.add_resource(InvitationReject, '/rejectinvitation')
api.add_resource(ProviderList, '/list_providers') #has filters

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
