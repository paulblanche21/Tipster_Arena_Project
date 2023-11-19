from unittest.mock import patch

# TODO: Add assertions based on your application's specific behavior


def test_on_join(client):
    # Arrange
    data = {'username': 'test_user'}

    # Act
    client.emit('join', data)

    # Assert
    # TODO: Add assertions based on your application's specific behavior


def test_on_leave(client):
    # Arrange
    data = {'username': 'test_user'}

    # Act
    client.emit('leave', data)

    # Assert
    # TODO: Add assertions based on your application's specific behavior


def save_message(username, msg):
    # TODO: Implement the logic to save the message 
    pass


@patch('TipsterArena.models.chatrooms.db.session')
def test_save_message(mock_db_session):
    # Arrange
    username = 'test_user'
    msg = 'Hello, World!'

    # Act
    save_message(username, msg)

    # Assert
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
