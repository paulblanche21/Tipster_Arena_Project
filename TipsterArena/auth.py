from flask import Blueprint, render_template, redirect, url_for, flash, session, current_app
from models.user import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from extensions import db, bcrypt, login_manager
from flask import current_app as app

auth_bp = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
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
        # Check if user already exists
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('An account with this email already exists.', 'warning')
            return redirect(url_for('auth.register'))

        # Hash the password and create a new user
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # Log the CSRF token for debugging
        current_app.logger.debug('CSRF Token submitted: %s', form.csrf_token.data)

        # Add the new user to the database
        try:
            app.logger.debug(f"Attempting to add user: {new_user.username}")
           # Log before adding the user
           
            db.session.add(new_user)
            db.session.commit()
            
            # Log after successful commit
            app.logger.info('New user committed to the database.')
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            app.logger.error('Failed to add new user to the database: %s', e)
            flash('An error occurred during registration. Please try again.', 'error')
            return redirect(url_for('auth.register'))

    return render_template('register.html', show_logo=False, form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()

            if user and user.check_password(password):
                session['user_id'] = user.user_id
                flash('Login successful!', 'success')
                return redirect(url_for('main.home'))
            else:
                flash('Incorrect email or password', 'danger')
        except Exception as e:
            current_app.logger.error(f"An error occurred during login: {e}")
            flash('An error occurred during login. Please try again.', 'error')
            return render_template('login.html', show_logo=False, form=form), 500
    else:
        # If the form is submitted but not valid, log the errors
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                current_app.logger.error(f"Error in {fieldName}: {err}")

    return render_template('login.html', show_logo=False, form=form)


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))
