import base64
import os
import secrets
from datetime import datetime
from datetime import timedelta
from flask import flash, url_for, redirect
from flask import Flask, g, render_template, session, request
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import current_user, login_required
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length
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
    db.init_app(app)  #
    bcrypt.init_app(app)
    cors.init_app(app)
    csrf.init_app(app)
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    from models.user import User
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
    return render_template('base.html',
                           g_font_awesome_nonce=font_awesome_nonce,
                           g_bootstrap_nonce=bootstrap_nonce)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


@app.route('/login', methods=['GET', 'POST'])
def login():
    from models.user import User
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


@app.route('/latest-tips')
def latest_tips():
    return render_template('latest-tips.html')


@app.route('/tipster-league-table')
def tipster_league_table():
    return render_template('tipster-league-table.html')


@app.route('/football-chat')
def football_chat():
    return render_template('football_chat.html',
                           hide_logo=True, is_chatroom=True)


@app.route('/horse-racing-chat')
def horse_racing_chat():
    return render_template('horse_racing_chat.html',
                           hide_logo=True, is_chatroom=True)


@app.route('/tennis-chat')
def tennis_chat():
    return render_template('tennis_chat.html',
                           hide_logo=True, is_chatroom=True)


@app.route('/golf-chat')
def golf_chat():
    return render_template('golf_chat.html', hide_logo=True, is_chatroom=True)


@app.route('/subscription-plans', methods=['GET'])
def view_subscription_plans():
    from models.user import SubscriptionPlan
    plans = SubscriptionPlan.query.all()
    return render_template('subscription_plans.html', plans=plans)


@app.route('/create-subscription-plan', methods=['GET', 'POST'])
def create_subscription_plan():
    from models.user import SubscriptionPlan
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        duration = request.form['duration']

        new_plan = SubscriptionPlan(name=name, price=price, duration=duration)
        db.session.add(new_plan)
        db.session.commit()

        flash('Subscription plan created successfully!', 'success')
        return redirect(url_for('view_subscription_plans'))

    return render_template('create_subscription_plan.html')


@app.route('/subscribe/<int:plan_id>', methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in
def subscribe(plan_id):
    from models.user import SubscriptionPlan, UserSubscription
    plan = SubscriptionPlan.query.get_or_404(plan_id)

    if request.method == 'POST':
        end_date = datetime.utcnow() + timedelta(days=plan.duration)

        subscription = UserSubscription(
            user_id=current_user.user_id,
            plan_id=plan.plan_id,
            end_date=end_date
        )
        db.session.add(subscription)
        db.session.commit()

        flash('Subscribed successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('subscribe.html', plan=plan)


# Print all registered routes
for rule in app.url_map.iter_rules():
    print(f'{rule.endpoint}: {rule}')

#######################################################################
#                      RUN PROGRAM
#######################################################################


# if __name__ == '__main__':
    # if app.config.get('FLASK_ENV') == "development":
         #socketio.run(app, debug=True)
    # else:
        #print("Running in production mode")
        #socketio.run(app)
app.run(debug=True)
