from flask import Flask, render_template, request, jsonify
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# In-memory message storage (replace with database in production)
chat_history = []

# HTML template (store in templates/index.html in production)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Chat Interface</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: system-ui, -apple-system, sans-serif;
        }
        
        body {
            background-color: #343541;
            color: #FFFFFF;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .chat-container {
            flex-grow: 1;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            width: 100%;
            overflow-y: auto;
            padding-bottom: 100px;
        }
        
        .message {
            padding: 20px;
            margin: 10px 0;
            border-radius: 5px;
            max-width: 100%;
        }
        
        .user-message {
            background-color: #444654;
        }
        
        .assistant-message {
            background-color: #343541;
        }
        
        .input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 20px;
            background-color: #343541;
            border-top: 1px solid #565869;
        }
        
        .input-wrapper {
            max-width: 800px;
            margin: 0 auto;
            position: relative;
        }
        
        .message-input {
            width: 100%;
            padding: 15px 60px 15px 15px;
            border-radius: 5px;
            border: 1px solid #565869;
            background-color: #40414f;
            color: white;
            font-size: 16px;
            resize: none;
            min-height: 52px;
            max-height: 200px;
            outline: none;
        }
        
        .send-button {
            position: absolute;
            right: 10px;
            bottom: 8px;
            background: none;
            border: none;
            color: #fff;
            cursor: pointer;
            padding: 8px;
            border-radius: 4px;
        }
        
        .send-button:hover {
            background-color: #565869;
        }
        
        .send-button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .typing-indicator {
            padding: 20px;
            color: #8e8ea0;
            display: none;
        }
    </style>
</head>
<body>
    <div class="chat-container" id="chatContainer"></div>
    <div class="typing-indicator" id="typingIndicator">Assistant is typing...</div>
    <div class="input-container">
        <div class="input-wrapper">
            <textarea 
                class="message-input" 
                id="messageInput" 
                placeholder="Type your message..."
                rows="1"
                autofocus
            ></textarea>
            <button class="send-button" id="sendButton" disabled>
                ➤
            </button>
        </div>
    </div>
    
    <script>
        const chatContainer = document.getElementById('chatContainer');
        const messageInput = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendButton');
        const typingIndicator = document.getElementById('typingIndicator');
        
        // Auto-resize textarea
        messageInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 200) + 'px';
            sendButton.disabled = !this.value.trim();
        });
        
        // Handle send button click
        async function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;
            
            // Add user message to chat
            addMessage('user', message);
            
            // Clear input
            messageInput.value = '';
            messageInput.style.height = 'auto';
            sendButton.disabled = true;
            
            // Show typing indicator
            typingIndicator.style.display = 'block';
            
            try {
                const response = await fetch('/send_message', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message }),
                });
                
                const data = await response.json();
                
                // Hide typing indicator
                typingIndicator.style.display = 'none';
                
                // Add assistant response to chat
                addMessage('assistant', data.response);
            } catch (error) {
                console.error('Error:', error);
                typingIndicator.style.display = 'none';
                addMessage('assistant', 'Sorry, there was an error processing your message.');
            }
        }
        
        function addMessage(role, content) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${role}-message`;
            messageDiv.textContent = content;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        // Event listeners
        sendButton.addEventListener('click', sendMessage);
        messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_TEMPLATE

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = data.get('message', '')
    
    # Store messages (replace with database in production)
    chat_history.append({
        'role': 'user',
        'content': user_message,
        'timestamp': datetime.now()
    })
    
    # Generate response (replace with actual AI model in production)
    assistant_response = f"Echo: {user_message}"
    
    chat_history.append({
        'role': 'assistant',
        'content': assistant_response,
        'timestamp': datetime.now()
    })
    
    return jsonify({'response': assistant_response})

if __name__ == '__main__':
    app.run(debug=True)

