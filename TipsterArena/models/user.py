import enum
from datetime import datetime
from flask_login import UserMixin
from extensions import db, bcrypt


class SubscriptionType(enum.Enum):
    """
    An enumeration representing the subscription types available for users.
    """
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
        """
        Sets the user's password by generating a hash of the given password using bcrypt.

        Args:
            password (str): The password to set.

        Returns:
            None
        """
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """
        Check if the provided password matches the user's password hash.

        Args:
            password (str): The password to check.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return bcrypt.check_password_hash(self.password, password)


    # Flask-Login integration
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        # Here you should write the logic to determine if a user is active
        return True  # Or return False if the user is not active

    @property
    def is_anonymous(self):
        return False


class Message(db.Model):
    """
    Represents a message sent in a chat room.

    Attributes:
        id (int): The unique identifier for the message.
        username (str): The username of the user who sent the message.
        message (str): The content of the message.
        timestamp (datetime): The date and time the message was sent.
        room_name (str): The name of the chat room the message was sent in.
        room_id (int): The unique identifier for the chat room.
        room (Room): The chat room the message was sent in.
    """
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
    """
    Represents a chat room in the Tipster Arena application.

    Attributes:
        room_id (int): The unique identifier for the room.
        name (str): The name of the room.
        description (str): A brief description of the room.
        created_at (datetime): The date and time the room was created.
        updated_at (datetime): The date and time the room was last updated.
        messages (list[Message]): A list of messages posted in the room.
    """
    __tablename__ = 'rooms'

    room_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    messages = db.relationship("Message", back_populates="room")
