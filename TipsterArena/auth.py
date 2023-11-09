from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask import current_app as app
from flask_wtf import FlaskForm
from flask_login import login_user
from sqlalchemy.exc import SQLAlchemyError
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from extensions import db, bcrypt, login_manager
from models.user import User


auth_bp = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    """
    Load a user from the database given a user ID.

    Args:
        user_id (int): The ID of the user to load.

    Returns:
        User: The User object corresponding to the given user ID, or None if no such user exists.
    """
    return User.query.get(int(user_id))


#######################################################################
#                 LOGIN AND REGISTRATION FORMS
#######################################################################
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegistrationForm(FlaskForm):
   
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

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('An account with this email already exists.', 'warning')
            return redirect(url_for('auth.register'))

        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data) 

        try:
            app.logger.debug(f"Attempting to add user: {new_user.username}")
            db.session.add(new_user)
            db.session.commit()
            app.logger.info('New user committed to the database.')
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except SQLAlchemyError as e:
            db.session.rollback()
            app.logger.error('Failed to add new user to the database: %s', e)
            flash('An error occurred during registration. Please try again.', 'error')
            return redirect(url_for('auth.register'))

    return render_template('register.html', show_logo=False, form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)  # This is the Flask-Login way to start a user session
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Incorrect email or password', 'danger')
    return render_template('login.html', show_logo=False, form=form)


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))
