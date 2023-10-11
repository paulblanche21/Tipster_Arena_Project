import os
import secrets
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


class Config:
    # Get the secret key from the environment variable and generate a new one if it doesn't exist
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(16))

    # Get the database URL from the environment variable and use a fallback if it doesn't exist
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'fallback_url')

    # You can add more configuration variables here as needed, for example:
    # MAIL_SERVER = os.getenv('MAIL_SERVER')
    # MAIL_PORT = int(os.getenv('MAIL_PORT', 25))
