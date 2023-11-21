const assert = require('assert');
const { Socket } = require('../static/js/socket.io');

describe('Socket', () => {
  let socket;

  beforeEach(() => {
    socket = new Socket();
  });

  it('should initialize with correct default values', () => {
    assert.strictEqual(socket.connected, false);
    assert.strictEqual(socket.recovered, false);
    assert.deepStrictEqual(socket.receiveBuffer, []);
    assert.deepStrictEqual(socket.sendBuffer, []);
    assert.deepStrictEqual(socket._queue, []);
    assert.strictEqual(socket._queueSeq, 0);
    assert.strictEqual(socket.ids, 0);
    assert.deepStrictEqual(socket.acks, {});
    assert.deepStrictEqual(socket.flags, {});
    assert.strictEqual(socket.io, undefined);
    assert.strictEqual(socket.nsp, undefined);
    assert.strictEqual(socket.auth, undefined);
    assert.deepStrictEqual(socket._opts, {});
  });

  it('should set connected to true when socket is connected', () => {
    socket.connected = true;
    assert.strictEqual(socket.connected, true);
  });

  it('should set recovered to true when connection state is recovered', () => {
    socket.recovered = true;
    assert.strictEqual(socket.recovered, true);
  });

  it('should add packets to receiveBuffer', () => {
    const packet1 = { type: 'packet1' };
    const packet2 = { type: 'packet2' };
    socket.receiveBuffer.push(packet1);
    socket.receiveBuffer.push(packet2);
    assert.deepStrictEqual(socket.receiveBuffer, [packet1, packet2]);
  });

  it('should add packets to sendBuffer', () => {
    const packet1 = { type: 'packet1' };
    const packet2 = { type: 'packet2' };
    socket.sendBuffer.push(packet1);
    socket.sendBuffer.push(packet2);
    assert.deepStrictEqual(socket.sendBuffer, [packet1, packet2]);
  });

  it('should add packets to the queue', () => {
    const packet1 = { type: 'packet1' };
    const packet2 = { type: 'packet2' };
    socket._addToQueue(packet1);
    socket._addToQueue(packet2);
    assert.deepStrictEqual(socket._queue, [packet1, packet2]);
  });

  it('should increment the queueSeq when adding packets to the queue', () => {
    const packet1 = { type: 'packet1' };
    const packet2 = { type: 'packet2' };
    socket._addToQueue(packet1);
    socket._addToQueue(packet2);
    assert.strictEqual(socket._queueSeq, 2);
  });

  it('should set the auth property if provided in the options', () => {
    const opts = { auth: 'some-auth' };
    const socketWithAuth = new Socket(undefined, undefined, opts);
    assert.strictEqual(socketWithAuth.auth, 'some-auth');
  });

  // Add more tests as needed
});