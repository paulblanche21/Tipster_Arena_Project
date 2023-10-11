from flask import (
    Blueprint, render_template, redirect, url_for,
    flash, jsonify
)
from flask_login import login_user, logout_user, login_required
from auth.forms import RegistrationForm, LoginForm
from model import User, db


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Create an instance of LoginForm
    errors = {}

    if form.validate_on_submit():  # Check if the form is submitted and valid
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            errors['email'] = 'Incorrect email or password'
            errors['password'] = 'Incorrect email or password'

    return render_template('base.html', form=form, errors=errors)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@auth.route('/register', methods=['POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        try:
            db.session.commit()
            return jsonify(success=True, message="Registration successful!")
        except Exception as e:
            db.session.rollback()
            print(e)  # Print the error or log it as needed
            return jsonify(
                success=False,
                message=("An error occurred during registration."
                         " Please try again later.")
                error=str(e)
            )

        # Else part
    else:
        return jsonify(
                success=False,
                message=("Registration failed. Please check your input"
                         " and try again."),
                errors=form.errors
        )
