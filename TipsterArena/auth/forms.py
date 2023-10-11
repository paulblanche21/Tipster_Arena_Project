from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields.core import BooleanField


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            Length(min=8)
        ]
    )
    
    agree_to_terms = BooleanField(
        'I agree to the terms and conditions',
        validators=[DataRequired()]
    )


def validate_password_confirm(form, field):
    if field.data != form.password.data:
        raise ValidationError("Password and Confirm Password fields must match.")
    