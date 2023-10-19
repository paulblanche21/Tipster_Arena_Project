# routes.py

from datetime import datetime
from flask import Blueprint, render_template
from flask_login import login_required, current_user


main = Blueprint('main', __name__)


@main.route('/dashboard')
@login_required
def dashboard():
    return 'Welcome, ' + current_user.username


@main.route('/')
def index():
    today = datetime.now().date()
    return render_template('index.html', today=today)


@main.route('/submit', methods=['POST'])
def submit_form():
    # Removed manual CSRF validation, Flask-WTF handles this
    return "Form submitted successfully"


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/football')
def football():
    return render_template('football.html', sport='football')


@main.route('/golf')
def golf():
    return render_template('golf.html', sport='golf')


@main.route('/horse_racing')
def horse_racing():
    return render_template('horse_racing.html', sport='horseracing')


@main.route('/tennis')
def tennis():
    return render_template('tennis.html', sport='tennis')


@main.route('/tipster-league-table')
def tipster_league_table():
    # This is a placeholder.
    tipsters = [
        {'username': 'john', 'sport': 'football', 'tips': 50, 'wins': 40},
        {'username': 'jane', 'sport': 'football', 'tips': 45, 'wins': 35},
        # add more football tipsters here...

        {'username': 'alice', 'sport': 'tennis', 'tips': 60, 'wins': 50},
        {'username': 'bob', 'sport': 'tennis', 'tips': 55, 'wins': 45},
        # add more tennis tipsters here...

        {'username': 'charlie', 'sport': 'golf', 'tips': 70, 'wins': 60},
        {'username': 'dave', 'sport': 'golf', 'tips': 65, 'wins': 55},
        # add more golf tipsters here...

        {'username': 'charlie', 'sport': 'horseracing',
         'tips': 70,
         'wins': 60},

        {'username': 'dave', 'sport': 'horseracing', 'tips': 65, 'wins': 55},
        # add more horse racing tipsters here...
    ]

    return render_template('tipster-league-table.html', tipsters=tipsters)


@main.route('/latest-tips')
def latest_tips():  # Consider updating the function name for consistency
    return render_template('latest-tips.html')


@main.route('/football-chat')
def football_chat():
    return render_template('football_chat.html', hide_logo=True)


@main.route('/horse-racing-chat')
def horse_racing_chat():
    return render_template('horse_racing_chat.html', hide_logo=True)


@main.route('/tennis-chat')
def tennis_chat():
    return render_template('tennis_chat.html', hide_logo=True)


@main.route('/golf-chat')
def golf_chat():
    return render_template('golf_chat.html', hide_logo=True)
