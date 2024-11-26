from flask_sqlalchemy import SQLAlchemy
from models import User
import re

def blank_fields(username, email, password, password_confirmation, bday):
    errors = []
    if not username:
        errors.append("The username field cannot be empty.")
    if not email:
        errors.append("The email field cannot be empty.")
    if not password:
        errors.append("The password field cannot be empty.")
    if not password_confirmation:
        errors.append("The passwords are not equal.")
    if not bday:
        errors.append("The date of birth field cannot be empty.")
    return errors
    
def existing_user(submitted_username):
    used_username = User.query.filter_by(username=submitted_username).first()
    if used_username:
        return ["This username is already in use. Please try another one."]
    return []

def password_confirmation(password_confirm, password):
    if password_confirm != password:
        return ["The passwords are not equal."]
    return []

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return ["The email address is not valid."]
    return []

def existing_email(submitted_email):
    used_email = User.query.filter_by(email=submitted_email).first()
    if used_email:
        return ["This email is already registered. Please try another one."]
    return []

def validate_registration(username, email, password, password_confirm, bday):
    errors = []
    errors.extend(blank_fields(username, email, password, password_confirm, bday))
    errors.extend(existing_user(username))
    errors.extend(password_confirmation(password_confirm, password))
    errors.extend(validate_email(email))
    errors.extend(existing_email(email))

    return errors

