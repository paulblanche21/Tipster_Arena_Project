# auth/__init__.py
from flask import Blueprint
from . import forms, views  # Ensure forms and views are loaded when the auth package is imported

# Creating a Blueprint for authentication-related routes
# This Blueprint will be registered to the main app
auth_bp = Blueprint('auth', __name__)

# TODO: Add any additional initialization or configuration specific to the auth package if needed
