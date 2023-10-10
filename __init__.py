import base64
import os
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from errors import handler
from auth import auth
from services.chat import handle_message, on_join, on_leave   # noqa: F401
from config import Config  # Importing Config
from routes import main
from model import User


app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
cors = CORS(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
csrf = CSRFProtect(app)
socketio = SocketIO(app)

# Register blueprints
app.register_blueprint(main)
app.register_blueprint(handler)
app.register_blueprint(auth, url_prefix='/auth')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# CSP and other configurations remain the same
# CSP
# Construct the CSP dictionary
csp = {
    'default-src': "'self'",
    'img-src': '*',
    'style-src': [
        "'self'", "'unsafe-inline'",
        'use.fontawesome.com', 'maxcdn.bootstrapcdn.com'
    ],
    'script-src': [
        "'self'", "'unsafe-inline'",
        'ajax.googleapis.com',
        'cdnjs.cloudflare.com',
        'maxcdn.bootstrapcdn.com'
    ],
    'font-src': "'self' use.fontawesome.com fonts.gstatic.com",
}

# Update the 'script-src' directive using an f-string
csp['script-src'] += [f"'nonce-{g.nonce}'"]

# Apply the CSP using Talisman
talisman = Talisman(app, content_security_policy=csp)


@app.before_request
def before_request():
    g.nonce = base64.b64encode(os.urandom(16)).decode('utf-8')


@app.after_request
def after_request(response):
    csp = {
        'default-src': "'self'",
        'script-src': f"'self' 'nonce-{g.nonce}'",
        'style-src': f"'self' 'nonce-{g.nonce}'",
        # Add other directives as needed
    }
    csp_str = "; ".join([f"{k} {v}" for k, v in csp.items()])
    response.headers['Content-Security-Policy'] = csp_str
    return response

# ... (your other code remains unchanged)

print("Flask application initialized")
