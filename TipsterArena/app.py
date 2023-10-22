import base64
import os
import re
import secrets
from datetime import datetime
from flask import flash, url_for, redirect
import bleach
from flask import Flask, g, render_template, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import current_user, login_required
from flask_migrate import Migrate
from flask_socketio import SocketIO, join_room, leave_room, send
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from markupsafe import escape
from sqlalchemy.orm import validates
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import ValidationError
from config import Config
from errors.handlers import handler


#######################################################################
#                  INITISATION EXTENSIONS
#######################################################################
app = None

db = SQLAlchemy()
bcrypt = Bcrypt()
cors = CORS()
csrf = CSRFProtect()
socketio = SocketIO()
migrate = Migrate()


def create_app(config_class=Config):
    print("Creating Flask app...")
    app = Flask(__name__)
    if app is None:
        print("Failed to create Flask app!")
        return None
    print("Loading configurations...")
    app.config.from_object(config_class)
    app.register_blueprint(handler)
    # Initialization of Extensions

    print("Initializing extensions...")
    db.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)
    csrf.init_app(app)
    socketio.init_app(app)
    migrate.init_app(app, db)

    print("Flask app created successfully!")
    Talisman(app, content_security_policy=app.config['CSP'])

    @app.before_request
    def before_request():
        g.nonce = base64.b64encode(os.urandom(16)).decode('utf-8')
        print(g.nonce)

    @app.after_request
    def after_request(response):
        # Check if nonce is set on g
        if hasattr(g, 'nonce'):
            # Adjusting CSP to include the nonce
            csp = response.headers.get('Content-Security-Policy')
            if csp is None:
                csp = ""
            csp += "; style-src 'self' use.fontawesome.com maxcdn.bootstrapcdn.com 'nonce-{}'".format(g.nonce)
            response.headers['Content-Security-Policy'] = csp
        return response
    return app


app = create_app(Config)

if app is None:
    print("The Flask app was not created!")
else:
    print("The Flask app was created successfully!")

#######################################################################
#                 LOGIN AND REGISSTRATION FORMS
#######################################################################


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    agree_to_terms = BooleanField(
        'I agree to the terms and conditions',
        validators=[DataRequired()]
    )


@app.route('/some_route')
def some_route():
    # Generate nonces
    font_awesome_nonce = secrets.token_hex(16)
    bootstrap_nonce = secrets.token_hex(16)

    # Render the template and pass the nonces as context variables
    return render_template('base.html', g_font_awesome_nonce=font_awesome_nonce, g_bootstrap_nonce=bootstrap_nonce)


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        form = LoginForm()

        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()

            if user and user.check_password(password):
                session['user_id'] = user.id
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Incorrect email or password', 'danger')

        return render_template('login.html', form=form)
    except Exception as e:
        print(f"An error occurred: {e}")
        # you can also log the error if you have logging setup
        return "An error occurred", 500  # or render an error template


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Print form data for debugging
        print(form.data)
        
        username = form.username.data
        password = form.password.data
        email = form.email.data

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)

        try:
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.',
                  'danger')
            print(e)  # Print exception for debugging

    # Print form errors for debugging
    print(form.errors)

    return render_template('register.html', form=form)


#######################################################################
#                 DATABASES MODELS
#######################################################################
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', back_populates='messages')

    # Additional fields
    email = db.Column(db.String(120))  # Email of the sender
    ip_address = db.Column(db.String(120))  # IP Address of the sender
    is_read = db.Column(db.Boolean, default=False)

    def __init__(self, username, message, email=None, ip_address=None):
        self.username = username
        self.message = message
        self.email = email
        self.ip_address = ip_address

    def mark_as_read(self):
        self.is_read = True
        db.session.commit()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Increased length
    first_name = db.Column(db.String(80), nullable=True)  # Optional
    last_name = db.Column(db.String(80), nullable=True)   # Optional
    date_joined = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)  # Optional
    subscription = db.relationship('Subscription',
                                   back_populates='user', uselist=False)
    messages = db.relationship('ChatMessage',
                               back_populates='user', lazy='dynamic')
    tips = db.relationship('Tip', back_populates='user')
    rankings = db.relationship('Ranking', back_populates='user')

    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValidationError('Invalid email address.')

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    user = db.relationship('User', back_populates='subscription')


class Tip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('User', back_populates='tips')


class Ranking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sport = db.Column(db.String(80), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', back_populates='rankings')


#######################################################################
#                               CHATROOMS
#######################################################################


MAX_MESSAGE_LENGTH = 515


@socketio.on('message')
def handle_message(msg):
    if len(msg) > MAX_MESSAGE_LENGTH:
        send('Message is too long!', broadcast=True)
        return

    msg = escape(msg)  # Escape HTML entities
    msg = bleach.clean(msg, strip=True)  # Clean the message content

    username = session.get('username', 'Anonymous')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mentions = re.findall(r'@\w+', msg)

    print('Message:', msg, 'Timestamp:', timestamp, 'Mentions:', mentions)

    message = Message(username=username, message=msg, timestamp=datetime.now())
    db.session.add(message)
    db.session.commit()

    send({'msg': msg, 'timestamp': timestamp,
          'mentions': mentions}, broadcast=True)


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send({"msg": username + " has joined the " + room + " room."}, room=room)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send({"msg": username + " has left the " + room + " room."}, room=room)

#######################################################################
#                               ROUTES
#######################################################################


@app.route('/dashboard')
@login_required
def dashboard():
    return 'Welcome, ' + current_user.username


@app.route('/')
def index():
    today = datetime.now().date()
    return render_template('index.html', today=today)


@app.route('/submit', methods=['POST'])
def submit_form():
    # Removed manual CSRF validation, Flask-WTF handles this
    return "Form submitted successfully"


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/football')
def football():
    return render_template('football.html', sport='football')


@app.route('/golf')
def golf():
    return render_template('golf.html', sport='golf')


@app.route('/horse_racing')
def horse_racing():
    return render_template('horse_racing.html', sport='horseracing')


@app.route('/tennis')
def tennis():
    return render_template('tennis.html', sport='tennis')


@app.route('/tipster-league-table')
def tipster_league_table():
    tipsters = Tip.query.all()
    return render_template('tipster-league-table.html', tipsters=tipsters)


@app.route('/latest-tips')
def latest_tips():  # Consider updating the function name for consistency
    return render_template('latest-tips.html')


@app.route('/chat')
def chat():
    return render_template('chat.html', hide_logo=True)


@app.route('/football-chat')
def football_chat():
    return render_template('football_chat.html', hide_logo=True)


@app.route('/horse-racing-chat')
def horse_racing_chat():
    return render_template('horse_racing_chat.html', hide_logo=True)


@app.route('/tennis-chat')
def tennis_chat():
    return render_template('tennis_chat.html', hide_logo=True)


@app.route('/golf-chat')
def golf_chat():
    return render_template('golf_chat.html', hide_logo=True)


# Print all registered routes
for rule in app.url_map.iter_rules():
    print(f'{rule.endpoint}: {rule}')

#######################################################################
#                      RUN PROGRAM
#######################################################################


#if __name__ == '__main__':
    #if app.config.get('FLASK_ENV') == "development":
       # socketio.run(app, debug=True)
    #else:
        #print("Running in production mode")
        #socketio.run(app)
app.run(debug=True)
