from flask_login import UserMixin
from datetime import datetime
from extensions import db, bcrypt
from sqlalchemy import Enum
import enum


class SubscriptionType(enum.Enum):
    MONTHLY = 1
    ANNUAL = 2

class User(UserMixin, db.Model):
    """
    Represents a user in the system.

    Attributes:
        user_id (int): The unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password (str): The hashed password of the user.
        subscription_status (bool): The subscription status of the user.
        created_at (datetime): The date and time when the user was created.
        updated_at (datetime): The date and time when the user was last updated.
        subscriptions (list): A list of the user's subscriptions.
    """

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    subscription_status = db.Column(db.Boolean, default=False)
    subscription_type = db.Column(db.Enum(SubscriptionType), nullable=False, default=SubscriptionType.MONTHLY)
    subscription_end_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    # Flask-Login integration
    def get_id(self):
        return str(self.user_id)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
     # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        # Here you should write the logic to determine if a user is active
        return True  # Or return False if the user is not active

    def is_anonymous(self):
        return False

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    room_name = db.Column(db.String, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.room_id'),
                        nullable=False)
    room = db.relationship("Room", back_populates="messages")


class Room(db.Model):
    __tablename__ = 'rooms'

    room_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    messages = db.relationship("Message", back_populates="room")


