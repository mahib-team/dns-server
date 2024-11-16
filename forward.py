import socket
import threading

# Define the source (incoming) and destination (forward) ports
SOURCE_PORT = 81
DEST_PORT = 8080
DEST_HOST = '192.168.82.7'  # Forward traffic to this IP address (can be changed)

def handle_client(client_socket):
    """Handles incoming client data and forwards it to the destination."""
    try:
        # Create a socket connection to the destination (forwarding to the desired port)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as forward_socket:
            forward_socket.connect((DEST_HOST, DEST_PORT))  # Connect to the destination server
            while True:
                # Receive data from the client (source port)
                data = client_socket.recv(4096)
                if not data:
                    break  # No data means the client has disconnected

                # Send the data to the destination
                forward_socket.sendall(data)

                # Receive the response from the destination and send it back to the client
                response = forward_socket.recv(4096)
                client_socket.sendall(response)

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def start_port_forwarding():
    """Starts the port forwarding server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
        listen_socket.bind(('0.0.0.0', SOURCE_PORT))  # Bind to all available interfaces on the source port
        listen_socket.listen(5)  # Set the backlog to 5 (max connections)

        print(f"Listening on port {SOURCE_PORT} and forwarding to {DEST_HOST}:{DEST_PORT}")

        while True:
            client_socket, addr = listen_socket.accept()
            print(f"Connection from {addr}")

            # Handle the client in a new thread
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()

if __name__ == "__main__":
    start_port_forwarding()
