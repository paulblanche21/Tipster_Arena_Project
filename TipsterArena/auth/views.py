from flask import (
    Blueprint, render_template, redirect, url_for, flash, session
)

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    from model import User, db
    from .forms import RegistrationForm, LoginForm
    form = LoginForm()
    errors = {}

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            errors['email'] = 'Incorrect email or password'
            errors['password'] = 'Incorrect email or password'

    return render_template('base.html', form=form, errors=errors)


@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))


@auth.route('/register', methods=['GET', 'POST'])  # Added 'GET' to allow loading the registration page
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
            flash('Registration successful!', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
            print(e)

    return render_template('register.html', form=form)
