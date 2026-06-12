from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_whatsapp_key!'
# cors_allowed_origins="*" se doosre phones easily connect ho payenge
socketio = SocketIO(app, cors_allowed_origins="*")

# Messages ko temporarily save karne ke liye list
chat_history = []

@app.route('/')
def index():
    # Chat page load hoga
    return render_template('index.html')

@socketio.on('message_from_client')
def handle_message(data):
    """Jab koi bhi phone se message bhejega, toh yeh sabhi ko real-time dikhega"""
    user = data.get('user', 'Anonymous')
    msg = data.get('message', '')
    time = data.get('time', '')
    
    msg_data = {'user': user, 'message': msg, 'time': time}
    chat_history.append(msg_data)
    
    # Broadcast matlab sabhi connected phones ko ek sath message bhejna
    emit('message_to_all', msg_data, broadcast=True)

if __name__ == '__main__':
    # Hum port badal kar 8000 kar dete hain (taki agar 5000 block ho toh dikkat na ho)
    print("\n" + "="*40)
    print(" WHATSAPP SERVER IS TRYING TO START...")
    print("="*40 + "\n")
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)