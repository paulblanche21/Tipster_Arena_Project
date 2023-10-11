import base64
import os
from urllib.parse import parse_qs as url_decode
from flask import Flask, g
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
import werkzeug.urls

from urllib.parse import urlencode
from urllib.parse import unquote as url_unquote
from config import Config
from errors.handlers import handler
from auth import auth
from model import User
from routes import main

# Initialize extensions
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
cors = CORS(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
socketio = SocketIO(app)

# Monkey-patching the url_encode function
werkzeug.urls.url_encode = urlencode
werkzeug.urls.url_decode = url_decode

# CSP Configuration
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
    'font-src': "'self' use.fontawesome.com fonts.gstatic.com"
}

# Update the 'script-src' directive using an f-string
csp['script-src'] += [f"'nonce-{g.nonce}'"]

Talisman(app, content_security_policy=csp)


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

# Corrected the indentation here
# Convert lists to strings


for directive, sources in csp.items():
    csp[directive] = ' '.join(sources)

# Register blueprints
app.register_blueprint(main)
app.register_blueprint(handler)
app.register_blueprint(auth, url_prefix='/auth')


@login_manager.user_loader
def load_user(user_id):
    user_id = url_unquote(user_id)
    return User.query.get(int(user_id))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)

online_users = set()
