# main.py

from flask import Blueprint, render_template
from flask_login import login_required
from datetime import datetime
from flask_login import current_user

# Define the blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Display the user dashboard."""
    return 'Welcome, ' + current_user.username


@main_bp.route('/')
def index():
    """Display the main homepage."""
    today = datetime.now().date()
    return render_template('index.html', today=today)


@main_bp.route('/submit', methods=['POST'])
def submit_form():
    """Handle form submissions."""
    # Removed manual CSRF validation, Flask-WTF handles this
    return "Form submitted successfully"


@main_bp.route('/about')
def about():
    """Display the about page."""
    return render_template('about.html')
