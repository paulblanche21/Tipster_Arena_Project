// Import the emoji picker (this will only work if chat.js is a module)
import 'https://unpkg.com/emoji-picker-element';

function createChatSocket() {
    console.log(`Attempting to connect to chat`);
    var socket = io.connect('http://127.0.0.1:5000/chat');
    var errorMessageElement = document.getElementById('error-message');

    socket.on('connect', function() {
        console.log(`Connected to chat`);
        socket.emit('join');
    });

    socket.on('connect_error', function(error) {
        console.error('Connection Error:', error);
    });

    socket.on('join_error', function(error) {
        console.error('Error joining chatroom:', error);
        errorMessageElement.textContent = 'Error joining chat: ' + error;
    });

    socket.on('error', function(error) {
        console.error('Socket error:', error);
        errorMessageElement.textContent = 'An error occurred: ' + error;
    });

    socket.on('disconnect', function(reason) {
        if (reason === 'io server disconnect') {
            // The server forced a disconnect
            errorMessageElement.textContent = 'Disconnected by the server';
        }
    });

    socket.on('message', function(data) {
        var li = document.createElement('li');
        li.appendChild(document.createTextNode(data.msg)); // Updated this line to handle the data object
        document.getElementById('messages').appendChild(li);

        // Auto-scroll to the bottom
        var messages = document.getElementById('messages');
        messages.scrollTop = messages.scrollHeight;

    });

    return {
        sendMessage: function() {
            var messageInput = document.getElementById('message');
            var message = messageInput.value.trim();  
            

            if (message === '') {
                errorMessageElement.textContent = 'Message cannot be empty';  
                return;
            }

            errorMessageElement.textContent = '';  
            socket.emit('message', {msg: message}, function(response) {
                if (response.error) {
                    errorMessageElement.textContent = response.error;
                    console.error('Error sending message:', response.error);
                } else {
                    console.log('Message sent:', message);
                }
            
            });
        }   
    };
}



// Create chat sockets
createChatSocket();

// Add the emoji picker code
const picker = document.querySelector('emoji-picker');
const input = document.getElementById('message');

picker.addEventListener('emoji-click', event => {
    input.value += event.detail.unicode;
});

