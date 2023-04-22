import socket
import threading
from datetime import datetime

HOST = "localhost"  # Standard loopback interface address (localhost)
PORT = 5555 # Port to listen on (non-privileged ports are > 1023), 5555 instead of 555 is just to allow non-privileged execution
ADDRESS = (HOST, PORT) # handling the address this way is easier
USERPASS = "CMPE322\0bilgiuni" # we will send user authentication as a null concatenated string

def authenticateClient(client_socket):
    # get data from the client
    data = client_socket.recv(1024)
    # return true if the client successfully authenticated
    return data.decode() == USERPASS

def handleClientOptions(client_socket):
    while (True):
            option = client_socket.recv(1024)
            match option.decode():
                case "date":
                    message = datetime.now.strftime("Date is: %d/%m/%Y")
                    client_socket.sendall(message.encode())
                case "time":
                    message = datetime.now.strftime("Time is: %H:%M:%S")
                    client_socket.sendall(message.encode())
                case "capTurkey":
                    message = "The capital of Turkey is Ankara"
                    client_socket.sendall(message.encode())
                case "quit":
                    message = "Bye bye."
                    client_socket.sendall(message.encode())
                    break

def handleClient(client_socket):
    # Send a welcome message to the client
    response = "Hello, client!\nPlease send your login information."
    client_socket.sendall(response.encode())
    # continually ask the client to authenticate until it authenticates successfully
    while (not authenticateClient()):
        response = "incorrect login information, failed to authenticate, try again."
        client_socket.sendall(response.encode())
    message = "you are OK, for asking me 'date, time, capTurkey, quit'"
    client_socket.sendall(message.encode())
    handleClientOptions(client_socket)
    client_socket.close()

# Create a server socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(ADDRESS)
    server_socket.listen()
    #print(server_socket)
    while (True):
        # Accept a new client connection
        client_socket, client_address = server_socket.accept()
        print(f"Received connection from {client_address}")

        # Start a new thread to handle the client connection
        client_thread = threading.Thread(target=handleClient, args=(client_socket))
        client_thread.start()
