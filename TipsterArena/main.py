# main.py
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from flask_login import current_user

# Define the blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Display the main homepage."""
    today = datetime.now().date()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    return render_template('index.html', today=today, logo=False)


@main_bp.route('/home')
@login_required
def home():
    """Display the user dashboard."""
    return render_template('home.html', username=current_user.username)


@main_bp.route('/submit', methods=['POST'])
def submit_form():
    """Handle form submissions."""
    return "Form submitted successfully"


@main_bp.route('/about')
def about():
    """Display the about page."""
    return render_template('about.html')


@main_bp.route('/terms-of-service')
def terms_of_service():
    """Display the terms of service page."""
    return render_template('termsofservice.html')


@main_bp.route('/contact')
def contact():
    """Display the contact page."""
    return render_template('contact.html')


@main_bp.route('/privacy-policy')
def privacy_policy():
    """Display the privacy policy page."""
    return render_template('privacypolicy.html')
