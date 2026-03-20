import os
from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)

# --- THE SPEED CONFIGURATION ---
# ping_timeout/interval: Keeps the "heartbeat" fast so the connection doesn't fall asleep.
# max_http_buffer_size: Limits the memory so it doesn't get clogged.
socketio = SocketIO(
    app, 
    cors_allowed_origins="*", 
    async_mode='eventlet',
    ping_timeout=5,
    ping_interval=2,
    engineio_logger=False,
    always_connect=True
)

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>TowerDesk Ultra-Low Latency</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin:0; background:#000; display:flex; justify-content:center; align-items:center; height:100vh; overflow:hidden; font-family:sans-serif;">
        
        <div id="status" style="position:fixed; top:10px; left:10px; color:#0f0; font-size:12px; background:rgba(0,0,0,0.5); padding:5px; border-radius:3px;">Connecting...</div>
        
        <img id="display" style="width:100%; max-width:1200px; cursor:crosshair; border:1px solid #333; display:none;">

        <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
        <script>
            const socket = io({
                transports: ['websocket'],
                upgrade: false
            });
            const img = document.getElementById('display');
            const status = document.getElementById('status');

            socket.on('connect', () => {
                status.innerText = "CONNECTED - STREAMING LIVE";
                status.style.color = "#0f0";
                img.style.display = "block";
            });

            socket.on('disconnect', () => {
                status.innerText = "DISCONNECTED - RECONNECTING...";
                status.style.color = "#f00";
            });

            socket.on('display', (data) => {
                if (data.image) {
                    // Optimized Blob handling
                    const blob = new Blob([new Uint8Array(data.image)], {type: 'image/jpeg'});
                    const url = URL.createObjectURL(blob);
                    const oldUrl = img.src;
                    
                    img.src = url;
                    
                    // Immediate memory release
                    if (oldUrl.startsWith('blob:')) {
                        URL.revokeObjectURL(oldUrl);
                    }
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
    # This sends the image to the browser as soon as it arrives
    emit('display', data, broadcast=True, include_self=False)

@socketio.on('mouse_action')
def handle_mouse(data):
    emit('execute', data, broadcast=True, include_self=False)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
