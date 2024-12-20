from flask_sqlalchemy import SQLAlchemy
from models import User
from datetime import datetime
import re

def blank_fields_registration(username, email, password, password_confirmation, bday): #added elif's to this block cuz i thought i would be a better UX if one error appears per try
    errors = []
    if not username:
        errors.append("The username field cannot be empty.") #errors.append will be used when the function got a list of errors to save
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
        return ["This username is already taken. Please choose another one."]
    return []

def password_confirmation(password_confirm, password):
    if password_confirm != password:
        return ["The passwords do not match."]
    return []

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return ["The email address provided is invalid."]
    return []

def existing_email(submitted_email):
    used_email = User.query.filter_by(email=submitted_email).first()
    if used_email:
        return ["This email is already in use. Please choose another one."]
    return []

def validate_password(password):
    errors = []
    #Simple password validation but it requires better UI in frontend (Future task) 
    if len(password) < 8: # This will be transfered to the frontend in the future and this code will return "Password must meet the security requirements" for when its submitted to server.
        errors.append("The password must be at least 8 characters long.")
    if not re.search(r'[A-Z]', password):
        errors.append("The password must contain at least one uppercase letter.")
    if not re.search(r'[a-z]', password):
        errors.append("The password must contain at least one lowercase letter.")
    if not re.search(r'[0-9]', password):
        errors.append("The password must contain at least one number.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("The password must contain at least one special character.")
    if re.search(r'\s', password):
        errors.append("The password cannot contain spaces.")
    
    return errors

def validade_age(submitted_bday):
    try:
        date_string = datetime.strptime(submitted_bday, "%Y-%m-%d") # takes the datetime object from the given string
        birth_year = date_string.year # splits the year from the rest
        current_year = datetime.now().year # takes the current time from the library
        age = current_year - birth_year # gets the age from user

        if age < 13:
            return ["You must be at least 13 years old to register."]
    except ValueError:
        return ["The date of birth is not valid. Please ensure it is in the correct format (YYYY-MM-DD)."]
    #print(date_string)
    return []

def validate_registration(username, email, password, password_confirm, bday):
    errors = []
    # executes first the blank spaces validation cuz if its blanks theres no reason to continue to others, besides it would print the same error twice on the user's screen
    errors.extend(blank_fields_registration(username, email, password, password_confirm, bday))
                  
    if not errors:
        errors.extend(existing_user(username))
        errors.extend(password_confirmation(password_confirm, password))
        errors.extend(validate_email(email))
        errors.extend(existing_email(email))
        errors.extend(validate_password(password))
        errors.extend(validade_age(bday))

    return errors

def blank_fields_login(username, password): #added elif's to this block cuz i thought i would be a better UX if one error appears per try
    errors = []
    if not username:
        errors.append("The username field cannot be empty.")
    elif not password:
        errors.append("The password field cannot be empty.")
    return errors

def null_username(submitted_username):
    inexistent_username = User.query.filter_by(username=submitted_username).first()
    if not inexistent_username:
        return ["This username is not recognized."]
    return []

def wrong_credentials(submitted_username, submitted_password):
    username = User.query.filter_by(username=submitted_username).first()
    if username and not username.check_password(submitted_password):
        return["The username or password you entered is incorrect."]    
    return[]

def validate_login(username, password):
    errors = []
    errors.extend(blank_fields_login(username, password))

    if not errors:
        errors.extend(null_username(username))
        errors.extend(wrong_credentials(username, password))

    return errors