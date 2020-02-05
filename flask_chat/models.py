''' database ORM models '''

from flask_chat import db, loginman
from flask_sqlalchemy import inspect
from datetime import datetime
from flask_login import UserMixin

# flask_login setup
@loginman.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

#----------------
# app db models |
#----------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='user-anonymous.png')
    user_messeges = db.relationship('Messege', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"


class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)
    channel_messeges = db.relationship('Messege', backref='channel', lazy=True)

    def __repr__(self):
        return self.title

    # make a counter for the channel messeges
    def chat_count(self):
        return len(self.channel_messeges)

    # usefull function to convert db object/instence to daictionary
    def as_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Messege(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'), nullable=False)
    messege = db.Column(db.String(), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Messege('{self.id}', '{self.timestamp}')"

    # usefull function to convert db object/instence to daictionary
    def as_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
