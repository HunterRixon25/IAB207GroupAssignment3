from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    comments = db.relationship('Comment', backref='user')

class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    eventCategory = db.Column(db.String(80))
    description = db.Column(db.String(250))
    image = db.Column(db.String(400))
    tickets = db.Column(db.String(3))
    ticketType = db.Column(db.String(80))
    ticketPrice = db.Column(db.String(80))
    eventLink = db.Column(db.String(80))
    address1 = db.Column(db.String(80))
    address2 = db.Column(db.String(80))
    city = db.Column(db.String(80))
    state = db.Column(db.String(80))
    postcode = db.Column(db.String(10))
    venueCapacity = db.Column(db.String(7))
    eventTags = db.Column(db.String(80))
    eventDateTime = db.Column(db.DateTime)
    comments = db.relationship('Comment', backref='events')

    def __repr__(self):
        return f"Name: {self.name}"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    events_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f"Comment: {self.text}"