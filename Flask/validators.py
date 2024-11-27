from flask_sqlalchemy import SQLAlchemy
from models import User
from datetime import datetime
import re

def blank_fields(username, email, password, password_confirmation, bday):
    errors = []
    if not username:
        errors.append("The username field cannot be empty.")
    elif not email:
        errors.append("The email field cannot be empty.")
    elif not password:
        errors.append("The password field cannot be empty.")
    elif not password_confirmation:
        errors.append("The passwords are not equal.")
    elif not bday:
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

def validade_age(submitted_bday):
    try:
        date_string = datetime.strptime(submitted_bday, "%Y-%m-%d") # takes the datetime object from the given string
        birth_year = date_string.year # splits the year from the rest
        current_year = datetime.now().year # takes the current time from the library
        age = current_year - birth_year # gets the age from user

        if age < 13:
            return ["You must be at least 13 years old to register."]
    except ValueError:
        return ["The date of birth is not in a valid format (DD-MM-YYYY)."]
    #print(date_string)
    return []

def validate_registration(username, email, password, password_confirm, bday):
    errors = []
    # executes first the blank spaces validation cuz if its blanks theres no reason to continue to others, besides it would print the same error twice on the user's screen
    errors.extend(blank_fields(username, email, password, password_confirm, bday))
                  
    if not errors:
        errors.extend(existing_user(username))
        errors.extend(password_confirmation(password_confirm, password))
        errors.extend(validate_email(email))
        errors.extend(existing_email(email))
        errors.extend(validade_age(bday))

    return errors

