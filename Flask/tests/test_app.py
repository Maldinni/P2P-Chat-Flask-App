import pytest
import sys
import os
import csv
import time
from datetime import datetime
from werkzeug.security import generate_password_hash

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add the parent directory to the system path to access app.py
from app import app, db, User
from flask import Flask

#Path to the parent directory
parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

#Path to the 'test_results' directory in the parent directory
new_directory = os.path.join(parent_directory, 'test_results')

#Create the directory if it doesn't exist
os.makedirs(new_directory, exist_ok=True)

#Function to generate a unique CSV filename based on the current date and time
def generate_csv_filename():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return os.path.join(new_directory, f'test_results_{timestamp}.csv')

#Function to save test results to a CSV file with a unique name
def save_test_result(test_name, execution_time, status, csv_file):
    """Saves test results to a CSV file."""
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            #Writes the header if the file is new
            writer.writerow(["Test Name", "Execution Time (seconds)", "Status", "Timestamp"])
        writer.writerow([test_name, execution_time, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

@pytest.fixture(scope='module')
def new_app():
    """Creates a test instance of the app and initializes the test database."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:%40Borabill13@localhost/chat_app_test' #Thats a local new database for tests, different from the application
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.create_all()  #Creates tables in the test database
        yield app
        db.session.remove()  #Removes the session after tests
        db.drop_all()  #Drops all tables after tests

@pytest.fixture
def new_user():
    """Creates or retrieves a test user."""
    # Check if the user already exists
    existing_user = User.query.filter_by(email="test@example.com").first()
    if existing_user is None:
        user = User(username="testuser", email="test@example.com", dob="2000-01-01")
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()
    else:
        user = existing_user #Use the existing user
    return user

#Function to measure the execution time of a test
def measure_time(test_func):
    """Measures the execution time of a test function."""
    start_time = time.time()  #Starts the timer to calculate the execution time
    result = test_func()  #Executes the test function
    execution_time = time.time() - start_time  #Calculates the elapsed time
    return result, execution_time

#Function that executes a test and save its result
def execute_and_save_test(test_func, test_name, csv_file):
    """Executes a test function and logs its results to a CSV file."""
    try:
        result, execution_time = measure_time(test_func)
        status = 'passed'
    except Exception as e:
        db.session.rollback()  #Rollback the transaction in case of error
        result = None
        execution_time = None
        status = 'failed'
        print(f"Error occurred during test {test_name}: {e}")
    
    #Saves the results to the CSV file
    save_test_result(test_name, execution_time, status, csv_file)

#Check if the home page redirects as expected
def test_home_redirect(new_app):
    client = new_app.test_client()
    csv_file = generate_csv_filename()
    execute_and_save_test(lambda: client.get('/'), 'test_home_redirect', csv_file)

#Verify behavior when registering with missing fields
def test_register_missing_fields(new_app):
    client = new_app.test_client()
    csv_file = generate_csv_filename()
    execute_and_save_test(lambda: client.post('/register', data={  
        'username': '',
        'email': 'test@example.com',
        'password': 'testpassword',
        'dob': '2000-01-01'
    }), 'test_register_missing_fields', csv_file)

#Verify successful registration
def test_register_success(new_app):
    client = new_app.test_client()
    csv_file = generate_csv_filename()
    execute_and_save_test(lambda: client.post('/register', data={  
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'newpassword',
        'dob': '1990-01-01'
    }), 'test_register_success', csv_file)

#Verify behavior when logging in with invalid credentials
def test_login_invalid_credentials(new_app, new_user):
    client = new_app.test_client()
    csv_file = generate_csv_filename()
    execute_and_save_test(lambda: client.post('/login', data={  
        'username': 'wronguser',
        'password': 'wrongpassword'
    }), 'test_login_invalid_credentials', csv_file)

#Verify successful login with valid credentials
def test_login_valid_credentials(new_app, new_user):
    client = new_app.test_client()
    csv_file = generate_csv_filename()
    execute_and_save_test(lambda: client.post('/login', data={  
        'username': 'testuser',
        'password': 'testpassword'
    }), 'test_login_valid_credentials', csv_file)

#Verify password hashing functionality
def test_password_hashing(new_user):
    csv_file = generate_csv_filename()
    execute_and_save_test(lambda: new_user.check_password('testpassword'), 'test_password_hashing', csv_file)
    execute_and_save_test(lambda: new_user.check_password('wrongpassword'), 'test_password_hashing_wrong', csv_file)
