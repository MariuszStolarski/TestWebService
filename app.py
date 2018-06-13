import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin
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

# other endpoints avalilable
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')

api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')

# allow these executions only when its called directly
if __name__ == '__main__':
	from db import db
	db.init_app(app)

	@app.before_first_request
	def create_tables():
		db.create_all()

	app.run(port=5000, debug = True)