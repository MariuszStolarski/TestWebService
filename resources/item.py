from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required

from models.item import ItemModel

class Item(Resource):

	# class global parser filter
	parser = reqparse.RequestParser()
	# lets filter only the expected arguments
	parser.add_argument('price', 
		type=float, 
		required=True, 
		help="This field cannot be left blank!")

	parser.add_argument('store_id',
		type=int, 
		required=True, 
		help="Every itme needs a store id!")

	@jwt_required() # to require authenticaiton via JWT
	def get(self, name):

		item = ItemModel.find_by_name(name)
		if item:
			return item.json()

		return {'message' : 'Item not found'}, 404

	

	def post(self, name):
		
		item = ItemModel.find_by_name(name)
		if item:
			return {'message':'An item with name {} already exist'.format(name)}, 400 # bad request

		data = Item.parser.parse_args()
		item = ItemModel(name, **data) # or ... data['price'], data['store_id'])
		
		try:
			item.save_to_db()
		except:
			return {'message' : 'An error occured saving the item.'}, 500 # internal server error
		
		return item.json(), 201 # item created

	def delete(self, name):

		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()
		
		return {'message':'item deleted'}

	def put(self, name):
		
		data = Item.parser.parse_args()

		item = ItemModel.find_by_name(name)
		if not item:
			# create new
			item = ItemModel(name, **data) # or ... data['price'], data['store_id'])
		else:
			# update
			item.price = data['price']

		item.save_to_db()
			
		return item.json()


class ItemList(Resource):

	def get(self):
		return {'items' : [item.json() for item in ItemModel.query.all()]} # or return {'item' : list(map(lambda x: x.json(), ItemModel.query.all()))}
