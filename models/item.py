from db import db

class ItemModel(db.Model):

	# usin SQLAlchemy prepare for Database
	__tablename__ = 'items'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80)) # with lengh limitation to 80 characters
	price = db.Column(db.Float(precision=2)) 

	store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
	store = db.relationship('StoreModel')

	def __init__(self, name, price, store_id):
		self.name = name
		self.price = price
		self.store_id = store_id

	def json(self):
		return {'name' : self.name, 'price' : self.price}

	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(name=name).first() # SQLAlechemy translate this to query: "SELECT * FROM items WHERE name = name LIMIT 1"

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()
