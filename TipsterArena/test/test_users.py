from flask import app
import pytest
from TipsterArena.extensions import db
from TipsterArena.models.user import User, SubscriptionPlan, UserSubscription, Message, Room

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # Create tables in the test database
            db.create_all()
        yield client
        # Cleanup after test
        with app.app_context():
            db.drop_all()

def test_user_model(client):
    # Create a user
    user = User(username="testuser", email="testuser@example.com")
    user.set_password("password123")

    db.session.add(user)
    db.session.commit()

    retrieved_user = User.query.filter_by(email="testuser@example.com").first()
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"
    assert retrieved_user.check_password("password123")
    assert not retrieved_user.check_password("wrongpassword")

def test_subscription_model(client):
    plan = SubscriptionPlan(name="Basic", price=9.99, duration=30)
    db.session.add(plan)
    db.session.commit()

    retrieved_plan = SubscriptionPlan.query.filter_by(name="Basic").first()
    assert retrieved_plan is not None
    assert retrieved_plan.price == 9.99

def test_user_subscription_model(client):
    user = User(username="testuser", email="testuser@example.com")
    user.set_password("password123")
    db.session.add(user)

    plan = SubscriptionPlan(name="Basic", price=9.99, duration=30)
    db.session.add(plan)
    db.session.commit()

    subscription = UserSubscription(user_id=user.user_id, plan_id=plan.plan_id, end_date=datetime.utcnow())
    db.session.add(subscription)
    db.session.commit()

    retrieved_subscription = UserSubscription.query.first()
    assert retrieved_subscription is not None
    assert retrieved_subscription.user.username == "testuser"
    assert retrieved_subscription.plan.name == "Basic"

def test_message_and_room_model(client):
    room = Room(name="chatroom1", description="Test chat room")
    db.session.add(room)
    db.session.commit()

    message = Message(username="testuser", message="Hello World", room_name="chatroom1", room_id=room.room_id)
    db.session.add(message)
    db.session.commit()

    retrieved_message = Message.query.first()
    assert retrieved_message is not None
    assert retrieved_message.username == "testuser"
    assert retrieved_message.message == "Hello World"
    assert retrieved_message.room.name == "chatroom1"

# Continue writing similar tests for other models and functionalities
