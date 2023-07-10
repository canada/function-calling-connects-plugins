document.getElementById('chat-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    sendMessage();
});

document.getElementById('user-input').addEventListener('keydown', (event) => {
    if (event.ctrlKey && event.key === 'Enter') {
    event.preventDefault();
    sendMessage();
    }
});

async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const question = userInput.value;
    userInput.value = '';

    addMessage('human', '人間', question);

    const response = await fetch('/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ question })
    });

    if (response.ok) {
    const data = await response.json();
    const answer = data.answer;
    addMessage('ai', 'AI', answer);
    } else {
    console.error('Error:', response.status);
    }
}

function addMessage(type, sender, text) {
    const chatContainer = document.getElementById('chat-container');
    const message = document.createElement('div');
    message.classList.add('message', type);

    const img = document.createElement('img');
    img.src = type === 'human' ? 'https://via.placeholder.com/40?text=Human' : 'https://via.placeholder.com/40/FFD700?text=AI';
    img.class = 'role';
    img.alt = sender;

    const bubble = document.createElement('div');
    bubble.classList.add('bubble');
    bubble.innerHTML = `${text}`;

    message.appendChild(img);
    message.appendChild(bubble);
    chatContainer.appendChild(message);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}