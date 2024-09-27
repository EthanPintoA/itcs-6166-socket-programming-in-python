from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread

from utils import (
    BUF_SIZE,
    SERVER_HOST,
    SERVER_PORT,
    connection_msg,
    disconnect_msg,
    sent_msg,
)

clients: set[socket] = set()
"""Keeps track of connected clients."""


def handle_client(client: socket, addr: tuple[str, int]):
    """Handles a client connection."""

    clients.add(client)  # Keep track of the connected client
    broadcast(connection_msg(addr), client)  # Broadcast that a new client has connected

    while True:
        try:
            # Receive messages from the client, decode the message and replace any unknown characters
            message = client.recv(BUF_SIZE).decode("utf-8", "replace")

            # If the client wants to exit, then break the loop
            if not message or message == "exit":
                break

            # Broadcast the received message to all clients
            broadcast(sent_msg(addr, message), client)
        except Exception:
            break

    # If client is disconnecting, then remove it
    clients.remove(client)
    broadcast(disconnect_msg(addr), client)
    client.close()


def broadcast(message: str, sender: socket):
    """Sends a message to all connected clients except the sender."""

    print(message)  # Make sure to print the message to the server console too

    for client in clients:
        if client != sender:  # Do not send the message to the sender
            try:
                # Send the message to the client and limit the message size
                client.send(message.encode("utf-8")[:BUF_SIZE])
            except Exception:
                # If the client is no longer connected then remove it
                clients.remove(client)
                broadcast(disconnect_msg(client.getpeername()), client)
                client.close()


def main():
    # Creates TCP socket using IPv4 addressing
    with socket(AF_INET, SOCK_STREAM) as server:
        # Bind the server to specified host and port
        server.bind((SERVER_HOST, SERVER_PORT))

        server.listen(5)  # Listen for incoming connections, queue up to 5
        print(f"Listening on {SERVER_HOST}:{SERVER_PORT}\n")

        try:
            # Accept a new connection, but ignore the address
            while True:
                conn, addr = server.accept()
                # Handle the client connection in a new thread
                Thread(target=handle_client, args=(conn, addr)).start()
        except Exception as e:
            print(f"[ERROR] {e}")

        # Close all client connections when the server is stopped.
        for client in clients:
            client.close()


if __name__ == "__main__":  # If the script is run directly
    main()
