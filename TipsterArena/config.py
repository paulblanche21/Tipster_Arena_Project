import os
import secrets
from dotenv import load_dotenv
import sys
import logging


# Print Python version for debugging
print(sys.version)

# Load environment variables from .env file
load_dotenv()


class Config:
    # Other configurations
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(16))
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
        ],
        'script-src': [
            "'self'",
            'ajax.googleapis.com',
            'cdnjs.cloudflare.com',
            'maxcdn.bootstrapcdn.com',
        ],
        'font-src': "'self' use.fontawesome.com fonts.gstatic.com"
    }


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG  
    

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = logging.WARNING  # Only warnings and errors in production
