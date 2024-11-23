from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User 

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xa6\xb6\\~*\xb87\xfew\xdd\xe7d`\xcc\xa1=\x17\xc6\xa2]\x9d\xd6\x89\xf6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:%40Borabill13@localhost/chat_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        submitted_username = request.form['username']
        submitted_email = request.form['email']
        submitted_password = request.form['password']

        existing_user = User.query.filter_by(username=submitted_username).first()
        if existing_user:
            flash("This username is already in use. Please try another one.", "danger")
            return redirect(url_for('register'))
        
        new_user = User(username=submitted_username, email=submitted_email)
        new_user.set_password(submitted_password)

        db.session.add(new_user)
        db.session.commit()

        flash("User created with success!", "success")
        return redirect(url_for("login"))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

if __name__ == "__main__":
    app.run(debug=True)