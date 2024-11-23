from flask_sqlalchemy import SQLAlchemy

# Inicializando o SQLAlchemy
db = SQLAlchemy()

# Modelo para usuários
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# Modelo para mensagens
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

# Função para inicializar o banco de dados
def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
