# Chat Room Using Sockets In Python

This original program creates a simple chat room using Python's socket and threading libraries, enabling multiple clients to communicate via a server.

## How to run

1. Run `python server.py`
2. Run multiple `python client.py`

I'm running Python 3.12.6, but it will likely work in previous versions.

### Usage

- Each client listens for user input continuously.
- Type your message and hit [Enter] to send.
- Type `exit` to disconnect from the server (note: you cannot send 'exit' as a message).

## Important Notes

- Messages are sent in plain text and are not secure.
