const io = require('socket.io-client');

// Replace with your server URL and port
const socket = io('http://127.0.0.1:8000');

socket.on('connect', () => {
    console.log('Connected to the server.');

    // Emit a test message
    socket.emit('message', {msg: 'Hello from client'});
});

socket.on('disconnect', () => {
    console.log('Disconnected from server.');
});

socket.on('message', (data) => {
    console.log('Message received:', data);
});

socket.on('error', (error) => {
    console.error('Error:', error);
});
