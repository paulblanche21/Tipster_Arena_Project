from flask import Blueprint
from . import forms, views  # Import the routes to ensure they get registered

auth_bp = Blueprint('auth', __name__)

# Any other initialization code specific to the auth package
