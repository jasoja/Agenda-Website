from vision_app import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime 
import sqlalchemy

class User(db.Model):
    email = db.Column(db.String(120), index=True, unique = True,primary_key=True)
    name = db.Column(db.String(120),  nullable=False)
    password_hash = db.Column(db.String(128))
    items = db.relationship('Item', backref='user',lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Item(db.Model):
    user_name = db.Column(db.String, db.ForeignKey('user.name')) # access the user's unique name
    task = db.Column(db.String(128), primary_key=True) # task list name
    date = db.Column(db.DateTime(timezone=True), default=datetime.now) # the date

