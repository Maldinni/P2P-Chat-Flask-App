const form = document.getElementById('message-form');
const input = document.getElementById('message-input');
const messagesDiv = document.getElementById('messages');

// Exemplo básico de evento para envio de mensagem
form.addEventListener('submit', (e) => {
    e.preventDefault();
    const message = input.value.trim();

    if (message) {
        const newMessage = document.createElement('div');
        newMessage.textContent = message;
        messagesDiv.appendChild(newMessage);

        // Limpa o input
        input.value = '';
    }
});
