from flask import Flask, request, jsonify, session, render_template
from datetime import datetime
import secrets
import time
import random

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Dictionary to hold all session data
all_sessions = {}

def generate_dummy_response(prompt):
    time.sleep(2)
    responses = [
        f"I understand you're asking about '{prompt}'. Here's what I know...",
        f"That's an interesting question about '{prompt}'. Let me explain...",
        f"Regarding '{prompt}', there are several important points to consider...",
        f"When it comes to '{prompt}', here's my analysis...",
    ]
    response = random.choice(responses)
    words = prompt.split()
    for word in words:
        if len(word) > 3:
            response += f" The concept of '{word}' is particularly relevant here."
    response += "\n\nWould you like me to elaborate on any specific aspect?"
    return response

@app.route('/')
def home():
    # Check if a session ID exists; if not, create one
    session_id = session.get('session_id')
    if not session_id:
        session_id = secrets.token_hex(8)
        session['session_id'] = session_id
        all_sessions[session_id] = []  # Initialize session history for this session

    # Render the home page with all stored sessions
    return render_template('comments.html', chat_history=all_sessions)

@app.route('/send_message', methods=['POST'])
def send_message():
    # Retrieve the current session ID
    session_id = session.get('session_id')
    if not session_id:
        # Generate a new session ID if none exists
        session_id = secrets.token_hex(8)
        session['session_id'] = session_id
        all_sessions[session_id] = []  # Initialize the conversation history for this session

    data = request.get_json()
    user_message = data.get('message', '')

    # Store the user message in the current session's history
    all_sessions[session_id].append({
        'role': 'user',
        'content': user_message,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

    assistant_response = generate_dummy_response(user_message)
    all_sessions[session_id].append({
        'role': 'assistant',
        'content': assistant_response,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

    return jsonify({'response': assistant_response})

@app.route('/get_conversation', methods=['GET'])
def get_conversation():
    session_id = request.args.get('session_id')
    history = all_sessions.get(session_id, [])
    return jsonify({'history': history})

@app.route('/new_chat', methods=['GET'])
def new_chat():
    # Generate a new session ID and initialize a new conversation history
    new_session_id = secrets.token_hex(8)
    session['session_id'] = new_session_id
    all_sessions[new_session_id] = []  # Create a new conversation history for this session
    return jsonify({'status': 'new session started', 'session_id': new_session_id})

if __name__ == '__main__':
    app.run(debug=True)
