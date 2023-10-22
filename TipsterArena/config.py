import os
import secrets
from dotenv import load_dotenv
import sys

# Print Python version for debugging
print(sys.version)

# Load environment variables from .env file
load_dotenv()


class Config:
    # Other configurations
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(16))
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')

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
