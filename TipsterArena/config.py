import os
import secrets
from dotenv import load_dotenv


load_dotenv()


db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(16))
    # Here we use the db variables to create the database URI
    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')

    # CSP Configuration should be part of the Config class
    CSP = {
        'default-src': "'self'",
        'img-src': '*',
        'style-src': [
            "'self'",
            'use.fontawesome.com', 'maxcdn.bootstrapcdn.com'
        ],
        'script-src': [
            "'self'",
            'ajax.googleapis.com',
            'cdnjs.cloudflare.com',
            'maxcdn.bootstrapcdn.com'
        ],
        'font-src': "'self' use.fontawesome.com fonts.gstatic.com"
        # You can't add the nonce here, it should be added during runtime, in the view or middleware
    }
