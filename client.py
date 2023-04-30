import socket
import os

HOST = "localhost"  # Standard loopback interface address (localhost)
PORT = 555 # Port to listen on 
ADDRESS = (HOST, PORT) # handling the address this way is easier

# function to clear the terminal
def clean():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')

# function that sends the password and name to the server and returns the answer
def authenticate(socket, user, password):
    userPass = user + "\0" + password
    socket.sendall(userPass.encode())
    return socket.recv(1024).decode()

# function that asks the server for a date and returns the answer
def getDate(socket):
    socket.sendall("date".encode())
    return socket.recv(1024).decode()

# function to ask the server for time and return it
def getTime(socket):
    socket.sendall("time".encode())
    return socket.recv(1024).decode()

# function to ask the server for the capital of turkey and returns it
def getCapTurkey(socket):
    socket.sendall("capTurkey".encode())
    return socket.recv(1024).decode()

# function that sends the quit command to the server and recieves the answer
def quitServer(socket):
    socket.sendall("quit".encode())
    return socket.recv(1024).decode()

# function to take input from the user for username and password
def getUserInput(socket):
    user = input("Username: ")
    password = input("Password: ")
    return authenticate(socket, user, password)

# function to authenticate a user with the server
def authenticateUser(socket):
    flag = True
    while (flag):
        answer = getUserInput(socket)
        print(answer)
        flag = (answer != "successfully authenticated\nyou are OK, for asking me 'date, time, capTurkey, quit'")

# print a menu and take choice input from the user
def userChoose(socket):
    option = input("1. date\n2. time\n3. capital of Turkey\n4. quit\nEnter the number of an option: ")
    clean()
    match option:
        case "1":
            return getDate(socket)
        case "2":
            return getTime(socket)
        case "3":
            return getCapTurkey(socket)
        case "4":
            return quitServer(socket)
        case _:
            print("\nerror: incorrect input\n")
            return userChoose(socket)

# establish connection with the server and enter the main loop
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        clientSocket.connect(ADDRESS)
        print(clientSocket.recv(1024).decode())
        authenticateUser(clientSocket)
        flag = True
        while (flag):
            message = userChoose(clientSocket)
            flag = message != "Bye bye."
            print(message)

main()
