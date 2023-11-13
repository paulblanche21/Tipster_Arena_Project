"""
 __init__.py file for extensions. Used to prevent cirluar imports.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_login import LoginManager


db = SQLAlchemy()
bcrypt = Bcrypt()
cors = CORS()
csrf = CSRFProtect()
migrate = Migrate()
socketio = SocketIO(logger=True, engineio_logger=True)
login_manager = LoginManager()
