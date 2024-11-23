from app import app, db  # Importando a aplicação e o objeto db
from models import User  # Importando os modelos (aqui estamos assumindo que o modelo 'User' está no arquivo models.py)

# Cria todas as tabelas no banco de dados com base nos modelos definidos
with app.app_context():  # Garantindo que estamos dentro do contexto da aplicação Flask
    db.create_all()  # Cria as tabelas no banco de dados
    print("Database created!")
