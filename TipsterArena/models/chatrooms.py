"""
This module defines a Flask-SocketIO chat application with single chat rooms.
It defines a ChatNamespace class that handles incoming chat messages,
user joining and leaving the chat room.
It also defines a save_message function that saves a message to the database.
The module registers the namespaces and defines the handle_message, on_join,
and on_leave functions that handle chat messages, user joining and leaving
the chat room respectively.
"""
from datetime import datetime
import re
import logging
import bleach
from flask import session
from flask_socketio import Namespace, send, join_room, leave_room
from markupsafe import escape
from sqlalchemy.exc import SQLAlchemyError
from extensions import db, socketio
from models.user import Message


logger = logging.getLogger(__name__)

# ChatNamespace class definition
CHATROOM_NAMESPACE = '/general-chat'


class ChatNamespace(Namespace):
    """
    A namespace for handling chat-related events.

    This namespace handles the following events:
    - on_message: handles incoming chat messages
    - on_join: handles a user joining the chat room
    - on_leave: handles a user leaving the chat room
    """
    def on_message(self, data):
        """
        Handle incoming message data.

        Args:
            data: The message data to be handled.
        """
        try:
            handle_message(data)
        except KeyError as e:
            logger.error("KeyError in on_message: %s", e)
            send({'error': 'Message format error'})
        except ValueError as e:
            logger.error("ValueError in on_message: %s", e)
            send({'error': 'Invalid value error'})
        except Exception as e:  # Fallback for unexpected exceptions
            logger.error("Unexpected error in on_message: %s", e)
            send({'error': 'An unexpected error occurred'})

    def on_join(self, data):
        """
        This method is called when a user joins a chatroom.
        It takes in the data of the user who joined and performs necessary
        actions.
        """
        username = session.get('username', 'Anonymous')
        try:
            on_join(data)
        except Exception as e:
            logger.error("Error in on_join: %s", e)
            # Handling for sending error to client, if necessary

    def on_leave(self, data):
        """
        Method called when a user leaves the chatroom.

        Args:
            data: The data associated with the user leaving the chatroom.
        """

        try:
            on_leave(data)
        except Exception as e:
            logger.error("Error in on_leave: %s", e)
            # Handling for sending error to client, if necessary


# Registering the namespaces
socketio.on_namespace(ChatNamespace(CHATROOM_NAMESPACE))

MAX_MESSAGE_LENGTH = 515


def save_message(username, msg):
    """
    Saves a message to the database.

    Args:
        username (str): The username of the message sender.
        msg (str): The message content.
        room (str): The name of the chat room.

    Returns:
        bool: True if the message was successfully saved, False otherwise.
    """
    message_instance = Message(username=username, message=msg,
                               timestamp=datetime.now(),
                               room=CHATROOM_NAMESPACE)

    try:
        db.session.add(message_instance)
        db.session.commit()
    except SQLAlchemyError as e:
        # Log the detailed error
        logger.error("Error saving message: %s, Data: {'username': %s, 'message': %s, 'room': %s}", e, username, msg, CHATROOM_NAMESPACE)
        db.session.rollback()
        return False
    return True


@socketio.on('message')
def handle_message(data):
    """
    Handles a chat message sent by a user.

    Args:
        data (dict): A dictionary containing the message and room data.

    Returns:
        None
    """

    msg = data['msg']
    if len(msg) > MAX_MESSAGE_LENGTH:
        send('Message is too long!', room=CHATROOM_NAMESPACE)
        return

    msg = escape(msg)
    msg = bleach.clean(msg, strip=True)
    username = session.get('username', 'Anonymous')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mentions = re.findall(r'@\w+', msg)

    if not save_message(username, msg):  # Removed the third argument
        send("An error occurred while sending your message. Please try again.",
             room=CHATROOM_NAMESPACE)
        return

    send({'msg': msg, 'timestamp': timestamp, 'mentions': mentions},
         room=CHATROOM_NAMESPACE)


@socketio.on('join')
def on_join(data):
    """
    Called when a user joins a chatroom.

    Args:
        data (dict): A dictionary containing additional data about the join event.
    """
    # Retrieve the username from the session, default to 'Anonymous' if not found
    username = session.get('username', 'Anonymous')
    logger.info(f"User joined: {username}")
    # Join the user to the chatroom namespace
    join_room(CHATROOM_NAMESPACE)
    
    print(f"User joined: {username}")

    # Send a message to the chatroom indicating that this user has joined
    send({"msg": f"{username} has joined the chatroom."}, room=CHATROOM_NAMESPACE)


@socketio.on('leave')
def on_leave(data):
    """
    Called when a user leaves a chatroom.

    Args:
        data (dict): A dictionary containing the username and room of the user
        leaving.

    Returns:
        None
    """
    username = data['username']
    leave_room(CHATROOM_NAMESPACE)
    send({"msg": username + " has left the chatroom."},
         room=CHATROOM_NAMESPACE)
