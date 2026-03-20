@app.route('/')
def index():
    return """
    <html>
        <body style="margin:0; background:black; display:flex; justify-content:center;">
            <img id="display" style="width:100%; max-width:1200px; cursor:crosshair;">
            <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
            <script>
                const socket = io();
                const img = document.getElementById('display');
                
                // 1. Receive Screen
                socket.on('display', (data) => {
                    img.src = 'data:image/jpeg;base64,' + data.image;
                });

                // 2. Send Clicks
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
