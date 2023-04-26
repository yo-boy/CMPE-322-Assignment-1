import socket
import threading
from datetime import datetime

HOST = "localhost"  # Standard loopback interface address (localhost)
PORT = 5555 # Port to listen on (non-privileged ports are > 1023), 5555 instead of 555 is just to allow non-privileged execution
ADDRESS = (HOST, PORT) # handling the address this way is easier
USERPASS = "CMPE322\0bilgiuni" # we will send user authentication as a null concatenated string

def authenticateClient(clientSocket):
    # get data from the client
    data = clientSocket.recv(1024)
    # return true if the client successfully authenticated
    return data.decode() == USERPASS

def handleClientRequests(clientSocket):
    while (True):
            option = clientSocket.recv(1024)
            match option.decode():
                case "date":
                    message = datetime.now().strftime("Date is: %d/%m/%Y \nyou are OK, for asking me 'date, time, capTurkey, quit'")
                    clientSocket.sendall(message.encode())
                case "time":
                    message = datetime.now().strftime("Time is: %H:%M:%S \nyou are OK, for asking me 'date, time, capTurkey, quit'")
                    clientSocket.sendall(message.encode())
                case "capTurkey":
                    message = "The capital of Turkey is Ankara \nyou are OK, for asking me 'date, time, capTurkey, quit'"
                    clientSocket.sendall(message.encode())
                case "quit":
                    message = "Bye bye."
                    clientSocket.sendall(message.encode())
                    break

def handleClient(clientSocket):
    try:
        # Send a welcome message to the client
        response = "Hello, client!\nPlease send your login information."
        clientSocket.sendall(response.encode())
        # continually ask the client to authenticate until it authenticates successfully
        while (not authenticateClient(clientSocket)):
            response = "incorrect login information, failed to authenticate, try again."
            clientSocket.sendall(response.encode())
        message = "successfully authenticated\nyou are OK, for asking me 'date, time, capTurkey, quit'"
        clientSocket.sendall(message.encode())
        handleClientRequests(clientSocket)
    except BrokenPipeError:
        pass
    clientSocket.close()

# Create a server socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    serverSocket.bind(ADDRESS)
    serverSocket.listen()
    #print(serverSocket)
    while (True):
        # Accept a new client connection
        clientSocket, clientAddress = serverSocket.accept()
        print(f"Received connection from {clientAddress}")

        # Start a new thread to handle the client connection
        clientThread = threading.Thread(target=handleClient, args=(clientSocket,))
        clientThread.start()
