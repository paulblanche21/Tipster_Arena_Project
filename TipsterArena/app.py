
# !/usr/bin/env python3

"""
Main application setup and entry point.
"""

import base64
import os
from flask import Flask, g
from flask_talisman import Talisman
import logging
from logging.handlers import RotatingFileHandler

from TipsterArena.config import DevelopmentConfig, ProductionConfig
from TipsterArena.extensions import db, bcrypt, cors, csrf, migrate, socketio
from TipsterArena.auth import auth_bp
from TipsterArena.subscriptions import subscriptions_bp
from TipsterArena.chat import chat_bp
from TipsterArena.errors.handlers import handler
from TipsterArena.sports import sports_bp
from TipsterArena.main import main_bp

#######################################################################
#                  INITISATION EXTENSIONS
#######################################################################


def create_app(config_name=None):
    """
    Create a Flask application using the app factory pattern.
    """

    app = Flask(__name__)

    # Load configuration
    if config_name is None:
        if os.environ.get('FLASK_ENV') == 'development':
            config_name = DevelopmentConfig
        else:
            config_name = ProductionConfig
    app.config.from_object(config_name)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, logger=True, engineio_logger=True)
    Talisman(app, content_security_policy=app.config['CSP'])

    #   Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(handler)
    app.register_blueprint(subscriptions_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(sports_bp)

    @app.before_request
    def before_request():
        """
        Generates a nonce for CSP before each request.
        """
        g.nonce = base64.b64encode(os.urandom(16)).decode('utf-8')
        print(g.nonce)

    @app.after_request
    def after_request(response):
        """
        Adjusts the CSP header to include the nonce after each request.
        """
        if hasattr(g, 'nonce'):
            # Adjusting CSP to include the nonce
            csp = response.headers.get('Content-Security-Policy')
            if csp is None:
                csp = ""
            csp += "; style-src 'self' use.fontawesome.com maxcdn.bootstrapcdn.com 'nonce-{}'".format(g.nonce)
            response.headers['Content-Security-Policy'] = csp
        return response
    # Setup logging based on configuration
    log_formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s [in %(pathname)s:%(lineno)d]')
    log_file = 'app.log'
    file_handler = RotatingFileHandler(log_file, maxBytes=100000, backupCount=10)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(app.config['LOG_LEVEL'])  # Set level from configuration

    app.logger.addHandler(file_handler)
    app.logger.setLevel(app.config['LOG_LEVEL'])  # Set level from configuration

    return app


app = create_app()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    # Running the app based on environment
    if app.config.get('FLASK_ENV') == "development":
        socketio.run(app, host='127.0.0.1', port=5000, debug=True)
    else:
        print("Running in production mode")
        socketio.run(app)
