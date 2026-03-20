import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
# The secret sauce: this allows the browser and the .exe to talk to the same spot
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@socketio.on('screen_data')
def handle_screen(data):
    # Sends the image from your friend's .exe to your browser
    emit('display', data, broadcast=True, include_self=False)

@socketio.on('mouse_action')
def handle_mouse(data):
    # Sends your clicks from the browser to your friend's .exe
    emit('execute', data, broadcast=True, include_self=False)

if __name__ == '__main__':
    # Render uses the 'PORT' environment variable
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
