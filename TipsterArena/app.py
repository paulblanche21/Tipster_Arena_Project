import base64
import os
from flask import Flask, g
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
cors = CORS()
csrf = CSRFProtect()
socketio = SocketIO()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)
    csrf.init_app(app)
    socketio.init_app(app)
    migrate.init_app(app, db)

    Talisman(app, content_security_policy=app.config['CSP'])

    @app.before_request
    def before_request():
        g.nonce = base64.b64encode(os.urandom(16)).decode('utf-8')

    @app.after_request
    def after_request(response):
        # Adjusting CSP to include the nonce
        csp = response.headers.get('Content-Security-Policy')
        csp += f"; script-src 'nonce-{g.nonce}'"
        response.headers['Content-Security-Policy'] = csp
        return response

    # Register blueprints
    from auth.views import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app


app = create_app()

if __name__ == '__main__':
    if app.config.get('FLASK_ENV') == "development":
        socketio.run(app, debug=True)
    else:
        print("Running in production mode")
        socketio.run(app)
