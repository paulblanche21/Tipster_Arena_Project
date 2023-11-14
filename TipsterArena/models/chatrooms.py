"""
This module defines a Flask-SocketIO chat application with multiple chat rooms.
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
from flask import session, request
from flask_socketio import Namespace, send, join_room, leave_room
from markupsafe import escape
from sqlalchemy.exc import SQLAlchemyError
from extensions import db, socketio
from models.user import Message

# CHATROOMS definition


CHATROOMS = [
    '/football-chat',
    '/golf-chat',
    '/tennis-chat',
    '/horse-racing-chat'
]

logger = logging.getLogger(__name__)


# ChatNamespace class definition
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
        room_namespace = request.namespace
        if room_namespace not in CHATROOMS:
            logger.error("Invalid namespace: %s", room_namespace)
            return
  
        try:
            handle_message(data)
        except Exception as e:
            logger.error("Error in on_message: %s", e)
            # You might want to send an error message back to the client
            send({'error': 'An unexpected error occurred'})

    def on_join(self, data):
        """
        This method is called when a user joins a chatroom.
        It takes in the data of the user who joined and performs necessary
        actions.
        """
        room_namespace = request.namespace
        if room_namespace not in CHATROOMS:
            logger.error("Invalid namespace: %s", room_namespace)
            return
    
        try:
            on_join(data)
        except Exception as e:
            logger.error(f"Error in on_join: {e}")
            # Handling for sending error to client, if necessary

    def on_leave(self, data):
        """
        Method called when a user leaves the chatroom.

        Args:
            data: The data associated with the user leaving the chatroom.
        """
        room_namespace = request.namespace
        if room_namespace not in CHATROOMS:
            logger.error("Invalid namespace: %s", room_namespace)
            return
        
        try:
            on_leave(data)
        except Exception as e:
            logger.error(f"Error in on_leave: {e}")
            # Handling for sending error to client, if necessary


# Registering the namespaces
for chatroom in CHATROOMS:
    socketio.on_namespace(ChatNamespace('/' + chatroom))

MAX_MESSAGE_LENGTH = 515


def save_message(username, msg, room):
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
                               timestamp=datetime.now(), room=room)

    try:
        db.session.add(message_instance)
        db.session.commit()
    except SQLAlchemyError as e:
        # Log the detailed error
        logger.error("Error saving message: %s, Data: {'username': %s, 'message': %s, 'room': %s}", e, username, msg, room)
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
    room_namespace = request.namespace

    msg = data['msg']
    room = data['room']

    if not msg or not room or room_namespace not in CHATROOMS:
        print("Message, room data, or namespace is invalid")
        return

    if len(msg) > MAX_MESSAGE_LENGTH:
        send('Message is too long!', room=room)
        return

    msg = escape(msg)
    msg = bleach.clean(msg, strip=True)
    username = session.get('username', 'Anonymous')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mentions = re.findall(r'@\w+', msg)

    if not save_message(username, msg, room):
        send("An error occurred while sending your message. Please try again.",
             room=room)
        return

    send({'msg': msg, 'timestamp': timestamp, 'mentions': mentions}, room=room)


@socketio.on('join')
def on_join(data):
    """
    Called when a user joins a chatroom.

    Args:
        data (dict): A dictionary containing the username and room information.

    Returns:
        None
    """
    username = data['username']
    room = data['room']
    room_namespace = request.namespace

    if room_namespace not in CHATROOMS:
        print("Invalid namespace")
        return

    join_room(room)
    send({"msg": username + " has joined the " + room + " room."}, room=room)


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
    room = data['room']
    room_namespace = request.namespace

    if room_namespace not in CHATROOMS:
        print("Invalid namespace")
        return

    leave_room(room)
    send({"msg": username + " has left the " + room + " room."}, room=room)
