import socket

HOST = "localhost"  # Standard loopback interface address (localhost)
PORT = 5555 # Port to listen on (non-privileged ports are > 1023), 5555 instead of 555 is just to allow non-privileged execution
ADDRESS = (HOST, PORT) # handling the address this way is easier

def authenticate(socket, user, password):
    userPass = user + "\0" + password
    socket.sendall(userPass.encode())
    return socket.recv(1024).decode()

def getDate(socket):
    socket.sendall("date".encode())
    return socket.recv(1024).decode()

def getTime(socket):
    socket.sendall("time".encode())
    return socket.recv(1024).decode()

def getCapTurkey(socket):
    socket.sendall("capTurkey".encode())
    return socket.recv(1024).decode()

def quitServer(socket):
    socket.sendall("quit".encode())
    return socket.recv(1024).decode()

def getUserInput(socket):
    user = input("Username: ")
    password = input("Password: ")
    return authenticate(socket, user, password)

def authenticateUser(socket):
    flag = True
    while (flag):
        answer = getUserInput(socket)
        print(answer)
        flag = (answer != "successfully authenticated\nare OK, for asking me 'date, time, capTurkey, quit'")




with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
    clientSocket.connect(ADDRESS)
    print(clientSocket.recv(1024).decode())
    authenticateUser(clientSocket)

    print(getDate(clientSocket))
    print(getTime(clientSocket))
    print(getCapTurkey(clientSocket))
    print(quitServer(clientSocket))
