import pytest
import sys
import os
import csv
import time
from datetime import datetime
from werkzeug.security import generate_password_hash

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Necessário para fazer o script ler o app.py
from app import app, db, User
from flask import Flask

# Caminho para o diretório pai
parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Caminho para a nova pasta no diretório pai
new_directory = os.path.join(parent_directory, 'test_results')

# Criação da pasta
os.makedirs(new_directory, exist_ok=True)

# Função para gerar o nome do arquivo CSV com base na data e hora
def generate_csv_filename():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return os.path.join(new_directory, f'test_results_{timestamp}.csv')

# Função para salvar os resultados no CSV com nome único
def save_test_result(test_name, execution_time, status, csv_file):
    """Salva os resultados dos testes em um arquivo CSV"""
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            # Escreve o cabeçalho apenas se o arquivo for novo
            writer.writerow(["Test Name", "Execution Time (seconds)", "Status", "Timestamp"])
        writer.writerow([test_name, execution_time, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

@pytest.fixture(scope='module')
def new_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:%40Borabill13@localhost/chat_app_test'
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.create_all()  # Cria as tabelas
        yield app
        db.session.remove()  # Remove a sessão após os testes
        db.drop_all()  # Exclui todas as tabelas após os testes

@pytest.fixture
def new_user():
    # Verificar se o usuário já existe
    existing_user = User.query.filter_by(email="test@example.com").first()
    if existing_user is None:
        user = User(username="testuser", email="test@example.com", dob="2000-01-01")
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()
    else:
        user = existing_user  # Usar o usuário existente
    return user

# Função para medir o tempo de execução do teste
def measure_time(test_func):
    start_time = time.time()  # Inicia o contador de tempo
    result = test_func()  # Executa o teste
    execution_time = time.time() - start_time  # Calcula o tempo de execução
    return result, execution_time

# Função para executar e registrar o resultado de cada teste
def execute_and_save_test(test_func, test_name, csv_file):
    try:
        result, execution_time = measure_time(test_func)
        status = 'passed'
    except Exception as e:
        db.session.rollback()  # Reverter a transação em caso de erro
        result = None
        execution_time = None
        status = 'failed'
        print(f"Error occurred during test {test_name}: {e}")
    
    # Salvar o resultado no CSV
    save_test_result(test_name, execution_time, status, csv_file)

def test_home_redirect(new_app):
    client = new_app.test_client()
    # Gerar um nome de arquivo CSV único para este teste
    csv_file = generate_csv_filename()
    execute_and_save_test(lambda: client.get('/'), 'test_home_redirect', csv_file)

def test_register_missing_fields(new_app):
    client = new_app.test_client()
    # Gerar um nome de arquivo CSV único para este teste
    csv_file = generate_csv_filename()
    execute_and_save_test(lambda: client.post('/register', data={  
        'username': '',
        'email': 'test@example.com',
        'password': 'testpassword',
        'dob': '2000-01-01'
    }), 'test_register_missing_fields', csv_file)

def test_register_success(new_app):
    client = new_app.test_client()
    # Gerar um nome de arquivo CSV único para este teste
    csv_file = generate_csv_filename()
    execute_and_save_test(lambda: client.post('/register', data={  
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'newpassword',
        'dob': '1990-01-01'
    }), 'test_register_success', csv_file)

def test_login_invalid_credentials(new_app, new_user):
    client = new_app.test_client()
    # Gerar um nome de arquivo CSV único para este teste
    csv_file = generate_csv_filename()
    execute_and_save_test(lambda: client.post('/login', data={  
        'username': 'wronguser',
        'password': 'wrongpassword'
    }), 'test_login_invalid_credentials', csv_file)

def test_login_valid_credentials(new_app, new_user):
    client = new_app.test_client()
    # Gerar um nome de arquivo CSV único para este teste
    csv_file = generate_csv_filename()
    execute_and_save_test(lambda: client.post('/login', data={  
        'username': 'testuser',
        'password': 'testpassword'
    }), 'test_login_valid_credentials', csv_file)

def test_password_hashing(new_user):
    # Gerar um nome de arquivo CSV único para este teste
    csv_file = generate_csv_filename()
    execute_and_save_test(lambda: new_user.check_password('testpassword'), 'test_password_hashing', csv_file)
    execute_and_save_test(lambda: new_user.check_password('wrongpassword'), 'test_password_hashing_wrong', csv_file)
