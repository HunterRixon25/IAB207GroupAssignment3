from . import db
from enum import Enum
#from sqlalchemy import Enum as SQLAlchemyEnum
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    phone = db.Column(db.String(16), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    events = db.relationship('Events', backref='user')
    comments = db.relationship('Comment', backref='user')
    tickets = db.relationship('Tickets', backref='user')

class EventState(Enum):
    OPEN = "Open"
    INVALID = "Invalid"
    SOLD = "Sold Out"
    CANCELLED = "Cancelled"

class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event_manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(80))
    eventCategory = db.Column(db.String(80))
    description = db.Column(db.String(250))
    image = db.Column(db.String(400))
    ticketCapacity = db.Column(db.Integer)
    ticketsSold = db.Column(db.Integer, default=0)
    ticketPrice = db.Column(db.Float)
    address1 = db.Column(db.String(80))
    address2 = db.Column(db.String(80))
    city = db.Column(db.String(80))
    state = db.Column(db.String(80))
    postcode = db.Column(db.String(10))
    venueCapacity = db.Column(db.Integer)
    eventDate = db.Column(db.Date)
    eventTime = db.Column(db.Time)
    eventState = db.Column(db.String(20))
    
    comments = db.relationship('Comment', backref='event')
    tickets = db.relationship('Tickets', backref='event')

    def __repr__(self):
        return f"Name: {self.name}"

class Tickets(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Ticket: {self.id}"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    events_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f"Comment: {self.text}"
