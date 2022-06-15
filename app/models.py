# Database models
# TODO - follow Stackoverflow guide.
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from app import db

class User(db.Model):
    # Basic fields
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(10),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    date_registered = db.Column() # date type?

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f'ID: {self.id}; user name: {self.username}'


#class Progress(db.Model):
  #  game1_complete = db.Column()
 #   game2_complete = db.Column()

