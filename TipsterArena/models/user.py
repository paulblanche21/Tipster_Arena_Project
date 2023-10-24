from datetime import datetime
from app import db
from app import bcrypt




class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    subscription_status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    subscriptions = db.relationship("UserSubscription", back_populates="user")

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class SubscriptionPlan(db.Model):
    __tablename__ = 'subscription_plans'

    plan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    user_subscriptions = db.relationship("UserSubscription",
                                         back_populates="plan")


class UserSubscription(db.Model):
    __tablename__ = 'user_subscriptions'

    subscription_id = db.Column(db.Integer,
                                primary_key=True,
                                autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    plan_id = db.Column(db.Integer,
                        db.ForeignKey('subscription_plans.plan_id'),
                        nullable=False)
    start_date = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow)
    end_date = db.Column(db.DateTime,
                         nullable=False)

    user = db.relationship("User",
                           back_populates="subscriptions")
    plan = db.relationship("SubscriptionPlan",
                           back_populates="user_subscriptions")


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    room = db.Column(db.String, nullable=False)
