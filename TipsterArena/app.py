import base64
import logging
import os
import re
import secrets

from flask import Flask, g, Blueprint
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager, login_required, UserMixin
from flask_socketio import SocketIO, join_room, leave_room, send
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from jinja2 import escape
from dotenv import load_dotenv

from config import Config  
from errors.handlers import handler
from auth import auth
from model import User
from routes import main
from services.chat import handle_message, on_join, on_leave   

# Application and Configuration
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
cors = CORS(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
socketio = SocketIO(app)
online_users = set()

# Register blueprints
app.register_blueprint(main)
app.register_blueprint(handler)
app.register_blueprint(auth, url_prefix='/auth')

# Configure logging
logging.basicConfig(level=logging.ERROR)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# CSP Configuration
csp = {
    # ... (same as your original code)
}

@app.before_request
def before_request():
    g.nonce = base64.b64encode(os.urandom(16)).decode('utf-8')
    csp['script-src'].append(f"'nonce-{g.nonce}'")

Talisman(app, content_security_policy=csp)

@app.after_request
def after_request(response):
    # ... (same as your original code)
    return response

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)
