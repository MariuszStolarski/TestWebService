import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'mySecretKeyHere' # or use: app.config['JWT_SECRET_KEY']
api = Api(app)

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity): # identity is what we pass to the create_access_token() in this case user.id
	if identity == 1: # TODO: Instead of card coding you should read from a coding file or database
		return {'is_admin' : True}
	return {'is_admin' : False}

@jwt.expired_token_loader
def expired_token_callabak():
	return jsonify({
		'description' : 'The token has expired',
		'error' : 'token_expired'
		}), 401

# some configurations:

@jwt.invalid_token_loader # invalid token was provided
def invalid_token_callaback(error):
	return jsonify ({
		'description' : 'Signature verification failed.',
		'error' : 'invalid_token'
		}), 401

@jwt.unauthorized_loader # no token were sent
def missing_token_callabak(error):
	return jsonify ({
		'description' : 'Request does not contain an access token.',
		'error' : 'authorization_required'
		}), 410

@jwt.needs_fresh_token_loader # token is correct but it is not the fresh one
def token_not_fresh_callaback(error):
	return jsonify ({
		'description' : 'The token is not fresh.',
		'error' : 'fres_token_required'
		}), 401

@jwt.revoked_token_loader # token is no longer valid (e.g. when user did log out)
def revoked_token_callaback(error):
	return jsonify ({
		'description' : 'The token has been revoked.',
		'error' : 'token_revoked'
		}), 401

# other endpoints avalilable
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')

api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')

# allow these executions only when its called directly
if __name__ == '__main__':
	from db import db
	db.init_app(app)

	@app.before_first_request
	def create_tables():
		db.create_all()

	app.run(port=5000, debug = True)