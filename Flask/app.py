from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from validators import validate_registration, validate_login
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xa6\xb6\\~*\xb87\xfew\xdd\xe7d`\xcc\xa1=\x17\xc6\xa2]\x9d\xd6\x89\xf6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:%40Borabill13@localhost/chat_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db)

@app.route('/')
#def test_connection():
    #try:
        # Executa uma simples consulta para testar a conexão com o banco de dados
        #result = db.session.execute(text("SELECT 1"))
        #db.session.commit()  # Confirma a consulta

        # Se a execução ocorrer sem erros, retornará um sucesso
        #return "Database connection is successful!"
    #except Exception as e:
        # Em caso de erro, a exceção será capturada e retornada
        #db.session.rollback()  # Garante o rollback em caso de erro
        #return f"Error connecting to the database: {str(e)}"

def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        submitted_username = request.form.get('username')
        submitted_email = request.form.get('email')
        submitted_password = request.form.get('password')
        submitted_password_confirm = request.form.get('password_confirm')
        submitted_bday = request.form.get('dob')

        errors =(validate_registration(submitted_username, submitted_email, submitted_password, submitted_password_confirm, submitted_bday))
        if errors:
            for error in errors:
                flash(error, "danger")
            return redirect(url_for('register'))

        new_user = User(username=submitted_username, email=submitted_email, dob=submitted_bday)
        new_user.set_password(submitted_password)

        db.session.add(new_user)
        db.session.commit()

        flash("User created with success!", "success")
        return redirect(url_for("login"))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        submitted_username = request.form.get('username')
        submitted_password = request.form.get('password')

        errors =(validate_login(submitted_username, submitted_password))
        if errors:
            for error in errors:
                flash(error, "danger")
            return redirect(url_for('login'))
        else:
            return redirect(url_for('chat'))

        #if not submitted_username or not submitted_password:
        #    flash("Username and password are required.", "danger")
        #    return redirect(url_for('login'))

        #existing_user = User.query.filter_by(username=submitted_username).first()
        #if existing_user and existing_user.check_password(submitted_password):
        #    flash('Login successful!', 'success')
        #    return redirect(url_for("chat"))
        #else:
        #    flash('Invalid username or password!', 'danger')
        #    return redirect(url_for("login"))

    return render_template('login.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

if __name__ == "__main__":
    app.run(debug=True)