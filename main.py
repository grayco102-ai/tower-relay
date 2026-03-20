import os
from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
# We added 'always_connect=True' to keep the pipe open
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet', always_connect=True)

@app.route('/')
def index():
    return """
    <html>
        <body style="margin:0; background:#111; display:flex; justify-content:center; align-items:center; height:100vh; overflow:hidden;">
            <img id="display" style="width:100%; max-width:1200px; cursor:crosshair; border: 2px solid #444;">
            <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
            <script>
                const socket = io({transports: ['websocket']});
                const img = document.getElementById('display');

                socket.on('display', (data) => {
                    // This handles the RAW BYTES coming from Python
                    const blob = new Blob([data.image], {type: 'image/jpeg'});
                    const url = URL.createObjectURL(blob);
                    const oldUrl = img.src;
                    img.src = url;
                    if (oldUrl.startsWith('blob:')) {
                        URL.revokeObjectURL(oldUrl);
                    }
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
    # The 'broadcast' sends it to your browser instantly
    emit('display', data, broadcast=True, include_self=False)

@socketio.on('mouse_action')
def handle_mouse(data):
    emit('execute', data, broadcast=True, include_self=False)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
