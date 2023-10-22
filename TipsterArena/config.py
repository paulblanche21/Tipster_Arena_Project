import os
import secrets
from dotenv import load_dotenv
import sys

# Print Python version for debugging
print(sys.version)

# Load environment variables from .env file
load_dotenv()


class Config:
    # Get environment variables
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')

    # Check for missing environment variables and raise error if any are missing
    missing_vars = [var for var in ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST'] if os.getenv(var) is None]
    if missing_vars:
        missing_vars_str = ', '.join(missing_vars)
        error_message = f"The following required environment variables are missing: {missing_vars_str}"
        raise EnvironmentError(error_message)

    # Other configurations
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(16))
    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
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


# Print out environment variables and database URI for debugging
print("DB Name:", Config.db_name)
print("DB User:", Config.db_user)
print("DB URI:", Config.SQLALCHEMY_DATABASE_URI)
