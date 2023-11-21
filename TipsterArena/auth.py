from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask import current_app as app
from flask_wtf import FlaskForm
from flask_login import login_user, logout_user
from sqlalchemy.exc import SQLAlchemyError
from wtforms import StringField, PasswordField, BooleanField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from models.user import User, SubscriptionType
from extensions import db, login_manager


auth_bp = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    """
    Load a user from the database given a user ID.

    Args:
        user_id (int): The ID of the user to load.

    Returns:
        User: The User object corresponding to the given user ID,
        or None if no such user exists.
    """
    return User.query.get(int(user_id))


#######################################################################
#                 LOGIN AND REGISTRATION FORMS
#######################################################################
class LoginForm(FlaskForm):
    """
    A form that allows users to log in with their email and password.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    """
    A form used for user registration.

    Attributes:
    - username (StringField): The username of the user.
    - email (StringField): The email of the user.
    - password (PasswordField): The password of the user.
    - confirm_password (PasswordField): The confirmation password of the user.
    - agree_to_terms (BooleanField): Whether the user
    - agrees to the terms and conditions.
    """

    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=8)]
    )
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

    # Add the subscription plan options
    subscription_plan = RadioField('Subscription Plan', choices=[
        ('monthly', 'Monthly - €5'),
        ('annual', 'Annual - €50')
    ], default='monthly')  # Default to monthly plan


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Renders the registration form and handles form submission. If the form is
    submitted successfully, a new user is
    created and added to the database.
    The user's subscription type and
    end date are set based on the chosen plan.
    """
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('An account with this email already exists.', 'warning')
            return redirect(url_for('auth.register'))

        new_user = User(
            username=form.username.data,
            email=form.email.data
        )
        new_user.set_password(form.password.data)
        # Set the subscription type based on the form data
        chosen_plan = form.subscription_plan.data
        if chosen_plan == 'monthly':
            new_user.subscription_type = SubscriptionType.MONTHLY
        elif chosen_plan == 'annual':
            new_user.subscription_type = SubscriptionType.ANNUAL

        # Calculate the subscription end date based on the chosen plan
        if new_user.subscription_type == SubscriptionType.MONTHLY:
            new_user.subscription_end_date = datetime.utcnow() + timedelta(days=30)
        elif new_user.subscription_type == SubscriptionType.ANNUAL:
            new_user.subscription_end_date = datetime.utcnow() + timedelta(days=365)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except SQLAlchemyError as e:
            db.session.rollback()
            app.logger.error(f'Failed to add new user to the database: {e}')
            flash('An error occurred during registration. Please try again.',
                  'error')

    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Logs in a user if the submitted form is valid and the email and password
    match a user in the database.

    Returns:
        If login is successful, redirects to the home page with a success
        message.
        If login fails, renders the login page with an error message.
    """
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Incorrect email or password', 'danger')
            return render_template('login.html', show_logo=False, form=form)
    return render_template('login.html', show_logo=False, form=form)


@auth_bp.route('/logout')
def logout():
    """
    Logs out the current user by removing their user_id from the session
    and redirecting to the index page.
    """
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))
