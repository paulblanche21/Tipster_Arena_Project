
# !/usr/bin/env python3

"""
Main application setup and entry point.
"""
import base64
import os
import logging
from logging.handlers import RotatingFileHandler
from ssl import SSLContext, PROTOCOL_TLS_SERVER
from flask import Flask, g
from flask_talisman import Talisman
from dotenv import load_dotenv
from flask_session import Session

from errors.handlers import handler
from config import DevelopmentConfig, ProductionConfig
from extensions import db, bcrypt, cors, csrf, migrate, socketio, login_manager
from auth import auth_bp
from chat import chat_bp
from sports import sports_bp
from main import main_bp

#######################################################################
#                  INITISATION EXTENSIONS
#######################################################################
ssl_context = None


def create_app(config_name=None):
    """
    Create a Flask application using the app factory pattern.
    """
    print("Creating app...")  # Print statement for debugging

    # Initialize Flask app
    app = Flask(__name__)
    print("Flask app initialized.")

    # Load configuration
    if config_name is None:
        if os.environ.get('FLASK_ENV') == 'development':
            config_name = DevelopmentConfig
            print("DevelopmentConfig loaded.")
        else:
            config_name = ProductionConfig
            print("ProductionConfig loaded.")
    app.config.from_object(config_name)

    # Initialize extensions
    load_dotenv()
    print("dotenv loaded.")
    db.init_app(app)
    print("Database initialized.")
    bcrypt.init_app(app)
    print("Bcrypt initialized.")
    cors.init_app(app, resources={r"/socket.io/*": {"origins": "*"}})
    print("CORS initialized.")
    csrf.init_app(app)
    print("CSRF protection initialized.")
    
    migrate.init_app(app, db)
    print("Migrate initialized.")
    socketio.init_app(app, async_mode='gevent', logger=True, engineio_logger=True)
    print("SocketIO initialized.")
    login_manager.init_app(app)
    print("Login manager initialized.")
    Session(app)
    print("Sessions initialized.")
    Talisman(app, content_security_policy=app.config['CSP'])
    print("Talisman initialized.")
    # Create database tables
    with app.app_context():
        db.create_all()
        print("Database tables created.")

    #   Register blueprints/.
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(handler)
    app.register_blueprint(chat_bp)
    app.register_blueprint(sports_bp)
    print("Blueprints registered.")
    #   Register before and after request functions

    @app.before_request
    def before_request():
        """
        Generates a nonce for CSP before each request.
        """
        g.nonce = base64.b64encode(os.urandom(16)).decode('utf-8')
        app.logger.debug("Before request, nonce generated: %s", g.nonce)

    @app.after_request
    def after_request(response):
        """
        Adjusts the CSP header to include the nonce after each request.
        """
        if hasattr(g, 'nonce'):
            # Adjusting CSP to include the nonce
            csp = response.headers.get('Content-Security-Policy', '')
            csp_with_nonce = f"{csp} 'nonce-{g.nonce}'"
            response.headers['Content-Security-Policy'] = csp_with_nonce
            app.logger.debug(
                 "After request, CSP updated with nonce: %s", g.nonce
            )
        else:
            app.logger.debug("After request, no nonce generated.")
        return response

    # Setup logging based on configuration
    log_formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s]: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    )
    log_file = 'app.log'
    file_handler = RotatingFileHandler(log_file, maxBytes=100000,
                                       backupCount=10)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(app.config['LOG_LEVEL'])
    # Set level from configuration

    app.logger.addHandler(file_handler)
    app.logger.setLevel(app.config['LOG_LEVEL'])
    # Set level from configuration

    @app.route('/test-logging')
    def test_logging():
        app.logger.info('This is an info message.')
        app.logger.warning('This is a warning message.')
        app.logger.error('This is an error message.')
        return 'Logging test'

    return app


app = create_app()

if __name__ == '__main__':
    print("Starting Flask server...")
    # Load SSL certificate and key
    ssl_context = SSLContext(PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(
        app.config['SSL_CERT_PATH'],
        app.config['SSL_KEY_PATH']
    )

    # Run the app in development mode
    app.run(host='0.0.0.0', port=8000, ssl_context=ssl_context, debug=True)

