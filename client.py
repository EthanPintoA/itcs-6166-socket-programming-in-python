from socket import AF_INET, SOCK_STREAM, socket
from threading import Event as ThreadingEvent
from threading import Thread

from utils import BUF_SIZE, SERVER_HOST, SERVER_PORT

# Shared event to stop the client
stop_event = ThreadingEvent()


def receive_messages(client: socket):
    """Receives messages from the server."""

    while not stop_event.is_set():
        try:
            msg = client.recv(BUF_SIZE)  # Receive message from the server
            if not msg:
                # Stop the client if connection is closed
                break

            print(msg.decode("utf-8"))
        except Exception:
            print("[ERROR] Connection to server lost.")
            break

    stop_event.set()  # Tell the send_messages function to stop


def send_messages(client: socket):
    """Sends messages to the server."""

    while not stop_event.is_set():
        message = input()
        try:
            if message.strip().lower() == "exit":
                print("[INFO] Exiting chat...")
                client.send(b"exit")  # Send exit message to the server
                break

            if message:
                # Send user message to the server
                client.send(message.encode("utf-8")[:BUF_SIZE])
        except Exception:
            print("[ERROR] Failed to send message.")
            break

    stop_event.set()  # Tell the receive_messages function to stop


def main():
    # Creates TCP socket using IPv4 addressing
    with socket(AF_INET, SOCK_STREAM) as client:
        client.connect((SERVER_HOST, SERVER_PORT))  # Connect to the server

        # Create threads for receiving and sending messages
        send_thread = Thread(target=send_messages, args=(client,))
        receive_thread = Thread(target=receive_messages, args=(client,))

        # Start threads
        send_thread.start()
        receive_thread.start()

        # Wait for threads to finish
        send_thread.join()
        receive_thread.join()


if __name__ == "__main__":  # If the script is run directly
    main()
