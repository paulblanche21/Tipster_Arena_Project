// Import the emoji picker (this will only work if chat.js is a module)
import 'https://unpkg.com/emoji-picker-element';

function createChatSocket(namespace) {
    console.log(`Attempting to connect to ${namespace}`);
    var socket = io.connect('http://127.0.0.1:5000/' + namespace);

    socket.on('connect', function() {
        console.log(`Connected to ${namespace}`);
        socket.emit('join');
    });

    socket.on('connect_error', function(error) {
        console.error('Connection Error:', error);
    });

    socket.on('disconnect', function(reason) {
        console.log('Disconnected:', reason);
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
            var errorMessageElement = document.getElementById('error-message');

            if (message === '') {
                errorMessageElement.textContent = 'Message cannot be empty';  
                return;
            }

            errorMessageElement.textContent = '';  
            socket.emit('message', {msg: message, room: namespace}, function(confirmation) {
                console.log('Message sent:', message, '| Confirmation:', confirmation);
            });
        }   
    };
}



// Create chat sockets for each namespace
var footballChat = createChatSocket('football-chat');
var golfChat = createChatSocket('golf-chat');
var tennisChat = createChatSocket('tennis-chat');
var horseRacingChat = createChatSocket('horse-racing-chat');


// Add the emoji picker code
const picker = document.querySelector('emoji-picker');
const input = document.getElementById('message');

picker.addEventListener('emoji-click', event => {
    input.value += event.detail.unicode;
});

