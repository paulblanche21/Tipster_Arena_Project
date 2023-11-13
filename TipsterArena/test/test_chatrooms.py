from datetime import datetime
from unittest.mock import patch, MagicMock

from models.chatrooms import handle_message


def test_handle_message():
    with patch('chatrooms.request') as mock_request, \
            patch('chatrooms.send') as mock_send, \
            patch('chatrooms.save_message') as mock_save_message:
        # Set up mock data
        mock_request.namespace = 'test_namespace'
        data = {
            'msg': 'Test message',
            'room': 'test_room'
        }
        session = {
            'username': 'test_user'
        }
        mock_request.namespace = 'test_namespace'
        mock_request.session = session

        # Test invalid data
        handle_message({'msg': '', 'room': '', 'namespace': 'test_namespace'})
        mock_send.assert_not_called()
        mock_save_message.assert_not_called()

        # Test message too long
        handle_message({'msg': 'a' * 1001, 'room': 'test_room', 'namespace': 'test_namespace'})
        mock_send.assert_called_once_with('Message is too long!', room='test_room')
        mock_save_message.assert_not_called()

        # Test valid message
        with patch('chatrooms.escape') as mock_escape, \
                patch('chatrooms.bleach.clean') as mock_clean, \
                patch('chatrooms.re.findall') as mock_findall:
            mock_escape.return_value = 'Test message'
            mock_clean.return_value = 'Test message'
            mock_findall.return_value = []
            mock_save_message.return_value = True

            handle_message(data)

            mock_send.assert_called_once_with({
                'msg': 'Test message',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'mentions': []
            }, room='test_room')
            mock_save_message.assert_called_once_with('test_user', 'Test message', 'test_room')