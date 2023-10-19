from datetime import datetime
from flask import session
import re
from flask_socketio import send, join_room, leave_room
from . import socketio, db  # Adjust imports based on your project
from jinja2 import escape
import bleach


MAX_MESSAGE_LENGTH = 515


@socketio.on('message')
def handle_message(msg):
    if len(msg) > MAX_MESSAGE_LENGTH:
        send('Message is too long!', broadcast=True)
        return

    msg = escape(msg)  # Escape HTML entities
    msg = bleach.clean(msg, strip=True)  # Clean the message content

    username = session.get('username', 'Anonymous')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mentions = re.findall(r'@\w+', msg)

    print('Message:', msg, 'Timestamp:', timestamp, 'Mentions:', mentions)

    message = Message(username=username, message=msg, timestamp=datetime.now())
    db.session.add(message)
    db.session.commit()

    send({'msg': msg, 'timestamp': timestamp,
          'mentions': mentions}, broadcast=True)


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


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', back_populates='messages')

    # Additional fields
    email = db.Column(db.String(120))  # Email of the sender
    ip_address = db.Column(db.String(120))  # IP Address of the sender
    is_read = db.Column(db.Boolean, default=False)

    def __init__(self, username, message, email=None, ip_address=None):
        self.username = username
        self.message = message
        self.email = email
        self.ip_address = ip_address

    def mark_as_read(self):
        self.is_read = True
        db.session.commit()
