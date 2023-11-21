const assert = require('chai').assert;
const sinon = require('sinon');
const io = require('socket.io-client');

// Import the function to be tested
const { createChatSocket } = require('../static/js/chat');

describe('createChatSocket', () => {
  let socket;
  let errorMessageElement;

  beforeEach(() => {
    // Create a mock socket object
    socket = {
      on: sinon.stub(),
      emit: sinon.stub()
    };

    // Create a mock error message element
    errorMessageElement = {
      textContent: ''
    };

    // Stub the io.connect method to return the mock socket object
    sinon.stub(io, 'connect').returns(socket);

    // Stub the document.getElementById method to return the mock error message element
    sinon.stub(document, 'getElementById').withArgs('error-message').returns(errorMessageElement);
  });

  afterEach(() => {
    // Restore the stubbed methods
    io.connect.restore();
    document.getElementById.restore();
  });

  it('should connect to the chat and emit a join event', () => {
    // Call the function to be tested
    createChatSocket();

    // Verify that the socket.on method is called with the 'connect' event and a callback function
    assert.isTrue(socket.on.calledWith('connect', sinon.match.func));

    // Call the callback function passed to socket.on('connect')
    socket.on.args[0][1]();

    // Verify that the socket.emit method is called with the 'join' event
    assert.isTrue(socket.emit.calledWith('join'));
  });

  it('should handle connection errors', () => {
    // Call the function to be tested
    createChatSocket();

    // Verify that the socket.on method is called with the 'connect_error' event and a callback function
    assert.isTrue(socket.on.calledWith('connect_error', sinon.match.func));

    // Call the callback function passed to socket.on('connect_error')
    socket.on.args[1][1]('Connection error message');

    // Verify that the error message is set correctly
    assert.strictEqual(errorMessageElement.textContent, 'An error occurred: Connection error message');
  });

  // Add more tests for other parts of the code...
});