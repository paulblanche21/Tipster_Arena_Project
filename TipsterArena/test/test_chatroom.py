import pytest
from TipsterArena.extensions import db
from TipsterArena.models.user import User, Message, Room


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

def test_user_registration(app, session):
    # Given
    from TipsterArena.models.user import User
    user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'securepassword'
    }

    # When
    new_user = User(username=user_data['username'], email=user_data['email'])
    new_user.set_password(user_data['password'])
    session.add(new_user)
    session.commit()

    # Then
    registered_user = User.query.filter_by(email=user_data['email']).first()
    assert registered_user is not None
    assert registered_user.check_password(user_data['password'])
def test_user_login(app, session):
    # Given
    from TipsterArena.models.user import User
    user_data = {
        'email': 'testuser@example.com',
        'password': 'securepassword'
    }
    user = User.query.filter_by(email=user_data['email']).first()

    # When & Then
    assert user is not None
    assert user.check_password(user_data['password'])
    
