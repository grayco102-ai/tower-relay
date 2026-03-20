import os
from flask import Flask
from flask_socketio import SocketIO, emit

# YOU NEED THESE TWO LINES FIRST:
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# NOW you can do the routes:
@app.route('/')
def index():
    return """
    <html>
        <body style="margin:0; background:black; display:flex; justify-content:center; align-items:center; height:100vh;">
            <img id="display" style="width:100%; max-width:1200px; cursor:crosshair; border: 2px solid #333;">
            <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
            <script>
                const socket = io();
                const img = document.getElementById('display');
                socket.on('display', (data) => {
                    img.src = 'data:image/jpeg;base64,' + data.image;
                });
                img.addEventListener('click', (e) => {
                    const rect = img.getBoundingClientRect();
                    const x = (e.clientX - rect.left) / rect.width;
                    const y = (e.clientY - rect.top) / rect.height;
                    socket.emit('mouse_action', {type: 'click', x: x, y: y});
                });
            </script>
        </body>
    </html>
    """

@socketio.on('screen_data')
def handle_screen(data):
    emit('display', data, broadcast=True, include_self=False)

@socketio.on('mouse_action')
def handle_mouse(data):
    emit('execute', data, broadcast=True, include_self=False)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
