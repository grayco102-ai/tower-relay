i<script>
    // Force the connection to be solid
    const socket = io({transports: ['websocket']});
    const img = document.getElementById('display');

    socket.on('display', (data) => {
        // Fix: Ensure we are looking at the 'image' property of the data object
        if (data.image) {
            // Convert the binary data to a Blob
            const blob = new Blob([data.image], {type: 'image/jpeg'});
            const url = URL.createObjectURL(blob);
            
            // Swap images
            const oldUrl = img.src;
            img.src = url;
            
            // Memory Management
            if (oldUrl.startsWith('blob:')) {
                URL.revokeObjectURL(oldUrl);
            }
        }
    });

    // Click handler
    img.addEventListener('click', (e) => {
        const rect = img.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width;
        const y = (e.clientY - rect.top) / rect.height;
        socket.emit('mouse_action', {type: 'click', x: x, y: y});
    });
</script>
