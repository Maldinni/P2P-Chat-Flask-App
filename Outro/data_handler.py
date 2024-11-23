import json
import os
from datetime import datetime

# Função para carregar dados do arquivo data.json
def load_data():
    if os.path.exists('data.json'):
        with open('data.json', 'r') as file:
            return json.load(file)
    else:
        # Se o arquivo não existir, cria um com estrutura inicial vazia
        return {"users": [], "messages": []}

# Função para salvar os dados no arquivo data.json
def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

# Função para adicionar um novo usuário
def add_user(username, email, password_hash):
    data = load_data()
    user_id = len(data["users"]) + 1  # Gerar um ID único para o usuário
    created_at = datetime.now().isoformat()

    for user in data["users"]:
        if user["username"] == username:
            print(f"Erro: O username '{username}' já está em uso.")
            return  # Se o usuário já existe, não adiciona

    for user in data["users"]:
        if user["email"] == email:
            print(f"Erro: O email '{email}' já está em uso.")
            return  # Se o usuário já existe, não adiciona

    user = {
        "user_id": user_id,
        "username": username,
        "email": email,
        "password_hash": password_hash,
        "created_at": created_at  # Coloque aqui o horário atual ou qualquer dado
    }
    data["users"].append(user)
    save_data(data)
    print(f"Usuário {username} cadastrado com sucesso!")

# Função para adicionar uma nova mensagem
def add_message(sender_id, receiver_id, content):
    data = load_data()
    message_id = len(data["messages"]) + 1  # Gerar um ID único para a mensagem
    message = {
        "message_id": message_id,
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "content": content,
        "timestamp": "2024-11-21T12:00:00"  # Coloque aqui o horário atual ou qualquer dado
    }
    data["messages"].append(message)
    save_data(data)

# Função para obter mensagens
def get_messages(user_id):
    data = load_data()
    messages = [msg for msg in data["messages"] if msg["sender_id"] == user_id or msg["receiver_id"] == user_id]
    return messages
