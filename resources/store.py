from flask_restful import Resource, reqparse
from models.store import StoreModel

class Store(Resource):

	# class global parser filter
	parser = reqparse.RequestParser()
	# TODO: an ampty pareser for now

	def get(self, name):
		store = StoreModel.find_by_name(name)
		if store:
			return store.json()

		return {'message' : 'Store not found'}, 404

	def post(self, name):
		if StoreModel.find_by_name(name):
			return {'message' : 'A store with name {} already exist'.format(name)}, 400

		store = StoreModel(name)
		try: 
			store.save_to_db()
		except:
			return {'message' : 'An error occured while createing the store.'}, 500

		return store.json(), 201

	def delete(self, name):
		store = StoreModel.find_by_name(name)

		if store:
			store.delete_from_db()
			return {'message' : 'Store deleted'}

		return {'message' : 'Store did not exist'}

	def put(self, name):
		
		data = Store.parser.parse_args()

		item = StoreModel.find_by_name(name)
		if not item:
			# create new
			item = StoreModel(name, **data)
		

		item.save_to_db()
			
		return item.json()


class StoreList(Resource):
	def get(self):
		return {'stores' : [store.json() for store in StoreModel.find_all()]}