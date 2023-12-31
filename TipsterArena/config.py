"""
    This class contains the configuration settings for the Flask application.
"""
import os
import sys
import logging
from dotenv import load_dotenv
import redis

# Print Python version for debugging
print(sys.version)

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    This class contains the configuration settings for the Flask application.
    """
    # Other configurations
    SECRET_KEY = os.getenv('SECRET_KEY')
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    LOG_LEVEL = logging.ERROR  # Default log level

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI',
                                        'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable track modifications

    CSP = {
        'default-src': "'self'",
        'img-src': '*',
        'style-src': [
            "'self'",
            'use.fontawesome.com',
            'maxcdn.bootstrapcdn.com',
            "'unsafe-inline'",
            # Add 'unsafe-inline' here if you're okay with the security risk
        ],
        'script-src': [
            "'self'",
            'ajax.googleapis.com',
            'cdnjs.cloudflare.com',
            'maxcdn.bootstrapcdn.com',
            'cdn.socket.io',
            'unpkg.com'
            # Add 'nonce-YOUR_RANDOM_STRING_HERE'; if you're using nonces
        ],
        'connect-src': [
            "'self'",
            'cdn.jsdelivr.net',
            'http://127.0.0.1:5000', 
            'http://127.0.0.1:8000'  # Add the required domain here
        ],
        'font-src': "'self' use.fontawesome.com fonts.gstatic.com",
         }
    # Redis session configuration
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


class DevelopmentConfig(Config):
    """
    Configuration class for development environment.
    """

    # SSL context setup
    SSL_CERT_PATH = os.getenv('SSL_CERT_PATH')
    SSL_KEY_PATH = os.getenv('SSL_KEY_PATH')
    DEBUG = True
    LOG_LEVEL = logging.DEBUG  # Debugging in development
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """
    Configuration class for production environment.

    Attributes:
        DEBUG (bool): Set to False to disable debugging.
        LOG_LEVEL (int): Set the logging level to WARNING
        to only show warnings and errors.
    """

    # SSL context setup
    SSL_CERT_PATH = os.getenv('SSL_CERT_PATH')
    SSL_KEY_PATH = os.getenv('SSL_KEY_PATH')
    DEBUG = False
    LOG_LEVEL = logging.WARNING  # Only warnings and errors in production
    SESSION_COOKIE_SECURE = True
