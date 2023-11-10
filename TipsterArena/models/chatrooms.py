from datetime import datetime
import re
import bleach
from flask import session, request
from flask_socketio import Namespace, send, join_room, leave_room
from markupsafe import escape
from extensions import db, socketio
from models.user import Message


# CHATROOMS definition


CHATROOMS = [
    'football-chat',
    'golf-chat',
    'tennis-chat',
    'horse-racing-chat'
]


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
        handle_message(data)

    def on_join(self, data):
        on_join(data)

    def on_leave(self, data):
        on_leave(data)


# Registering the namespaces
for chatroom in CHATROOMS:
    socketio.on_namespace(ChatNamespace('/' + chatroom))


MAX_MESSAGE_LENGTH = 515


def save_message(username, msg, room):
    message_instance = Message(username=username, message=msg,
                               timestamp=datetime.now(), room=room)

    try:
        db.session.add(message_instance)
        db.session.commit()
    except Exception as e:
        print(f"An error occurred while saving the message: {e}")
        db.session.rollback()
        return False
    return True


@socketio.on('message')
def handle_message(data):
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
    username = data['username']
    room = data['room']
    room_namespace = request.namespace

    if room_namespace not in CHATROOMS:
        print("Invalid namespace")
        return

    leave_room(room)
    send({"msg": username + " has left the " + room + " room."}, room=room)
