import socket
import threading

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 5555  # Port to listen on (non-privileged ports are > 1023)
ADDRESS = (HOST, PORT)
USERPASS = "CMPE322\0bilgiuni"

def authenticateClient(client_socket):
    data = client_socket.recv(1024)
    return data.decode() == USERPASS

def handleClient(client_socket):
    # Send a welcome message to the client
    response = "Hello, client!\nPlease send you login information."
    client_socket.sendall(response.encode())
    while (!authenticateClient()):
        response = "incorrect login information, failed to authenticate, try again."
        client_socket.sendall(response.encode())
    # TODO handle client after authentication
    client_socket.close()


# Create a server socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDRESS)

while (True):
    # Accept a new client connection
    client_socket, client_address = server_socket.accept()
    print(f"Received connection from {client_address}")

    # Start a new thread to handle the client connection
    client_thread = threading.Thread(target=handleClient, args=(client_socket))
    client_thread.start()


server_socket.close()
