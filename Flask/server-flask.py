from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send, emit
from flask import send_from_directory
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Conexão com o banco de dados SQLite
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                       id INTEGER PRIMARY KEY,
                       username TEXT,
                       message TEXT
                    )''')
    conn.commit()
    conn.close()

@app.route('/history', methods=['GET'])
def get_history():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username, message FROM messages")
    messages = cursor.fetchall()
    conn.close()
    return jsonify(messages)

@app.route('/')
def home():
    return "Bem-vindo ao meu servidor Flask!"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

@socketio.on('message')
def handle_message(data):
    print(f"Message received: {data}")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (username, message) VALUES (?, ?)", 
                   (data['username'], data['message']))
    conn.commit()
    conn.close()
    send(data, broadcast=True)

@app.route('/add_user', methods=['POST'])
def add_user_route():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password_hash = data['password_hash']  # No caso de senhas, não armazene a senha em texto simples.
    
    add_user(username, email, password_hash)
    return jsonify({"message": "Usuário adicionado com sucesso!"})

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    content = data['content']
    
    add_message(sender_id, receiver_id, content)
    return jsonify({"message": "Mensagem enviada!"})

@app.route('/get_messages/<int:user_id>', methods=['GET'])
def get_user_messages(user_id):
    messages = get_messages(user_id)
    return jsonify(messages)

if __name__ == '__main__':
    init_db()
    socketio.run(app, host='0.0.0.0', port=5000)
