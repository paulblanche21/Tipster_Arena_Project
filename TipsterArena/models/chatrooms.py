#######################################################################
#                               CHATROOMS
#######################################################################
from datetime import datetime
from app import db
import bleach 
import re
from flask import session
from flask_socketio import SocketIO
from flask_socketio import send, join_room, leave_room
from markupsafe import escape
from app import socketio



socketio = SocketIO(app)

MAX_MESSAGE_LENGTH = 515


@socketio.on('message')
def handle_message(data):
    msg = data['msg']
    room = data['room']  # Ensure the frontend sends the room info along with the message
    
    if not msg or not room:
        print("Message or room data is missing")
        return

    if len(msg) > MAX_MESSAGE_LENGTH:
        send('Message is too long!', room=room)
        return

    msg = escape(msg)  # Escape HTML entities
    msg = bleach.clean(msg, strip=True)  # Clean the message content
    username = session.get('username', 'Anonymous')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mentions = re.findall(r'@\w+', msg)

    print('Message:', msg, 'Timestamp:', timestamp, 'Mentions:', mentions)

    message = Message(username=username, message=msg, timestamp=datetime.now(), room=room)
    try:
        db.session.add(message)
        db.session.commit()
    except Exception as e:
        print(f"An error occurred while saving the message: {e}")
        db.session.rollback()
        send("An error occurred while sending your message. Please try again.", room=room)
        return


    send({'msg': msg, 'timestamp': timestamp,
          'mentions': mentions}, room=room)


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send({"msg": username + " has joined the " + room + " room."}, room=room)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send({"msg": username + " has left the " + room + " room."}, room=room)
