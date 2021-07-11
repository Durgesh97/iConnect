from db import db
from datetime import datetime

class Product(db.Model):
	pro_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	description= db.Column(db.String(250), nullable=True)
	price= db.Column(db.String(200), nullable=False)
	filename = db.Column(db.Text, nullable=False, unique=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	def __repr__(self):
		return '<Name %r>' % self.name