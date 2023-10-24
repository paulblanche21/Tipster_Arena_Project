function createChatSocket(namespace) {
    var socket = io.connect('http://127.0.0.1:5000/' + namespace);

    socket.on('connect', function() {
        socket.emit('join');
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
            socket.emit('message', {msg: message, room: namespace}); // Added room data when emitting the message
            messageInput.value = '';
        }
    };
}

// Create chat sockets for each namespace
var footballChat = createChatSocket('football-chat');
var golfChat = createChatSocket('golf-chat');
var tennisChat = createChatSocket('tennis-chat');
var horseRacingChat = createChatSocket('horse-racing-chat');
