from app import db, bcrypt
from datetime import datetime
from sqlalchemy.orm import validates


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Increased length
    first_name = db.Column(db.String(80), nullable=True)  # Optional
    last_name = db.Column(db.String(80), nullable=True)   # Optional
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Optional
    subscription = db.relationship('Subscription', back_populates='user', uselist=False)
    messages = db.relationship('ChatMessage', back_populates='user', lazy='dynamic')
    tips = db.relationship('Tip', back_populates='user')
    rankings = db.relationship('Ranking', back_populates='user')

    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email   # Replace this with more comprehensive validation
        return email

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    user = db.relationship('User', back_populates='subscription')


class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('User', back_populates='messages')


class Tip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('User', back_populates='tips')


class Ranking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sport = db.Column(db.String(80), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', back_populates='rankings')
