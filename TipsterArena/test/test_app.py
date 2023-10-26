import pytest
from TipsterArena.app import app, db
from TipsterArena.models.user import User, SubscriptionPlan

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

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    # replace 'Today is:' with some known text from your 'index.html'
    assert b"Today is:" in response.data

def test_about(client):
    response = client.get('/about')
    assert response.status_code == 200
    # replace 'About TipsterArena' with some known text from your 'about.html'
    assert b"About TipsterArena" in response.data

def test_register(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data

    # Test registration
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword',
        'confirm_password': 'testpassword',
        'agree_to_terms': True
    })
    assert response.status_code == 302  # Expecting a redirect after successful registration
    assert b"Location: /login" in response.headers  # Expecting a redirect to login page

    # Confirm user is added to database
    user = User.query.filter_by(email='test@example.com').first()
    assert user is not None

def test_login(client):
    # Add a user first to test login
    user = User(username='testuser', email='test@example.com')
    user.set_password('testpassword')
    db.session.add(user)
    db.session.commit()

    # Test login
    response = client.post('/login', data={'email': 'test@example.com', 'password': 'testpassword'})
    assert response.status_code == 302  # Expecting a redirect after successful login
    assert b"Location: /index" in response.headers  # Expecting a redirect to index page

# You can continue writing similar tests for other routes
