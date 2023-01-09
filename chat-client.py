import socket
import select
import sys

HOST = "127.0.0.1" 
PORT = 5000

# Creating a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# Establishing a connection with the server
print("Connection Status: Waiting")
server.connect((HOST, PORT))
status = server.recv(1024) # On the server side as soon as the connection is established, we send a connect status message to the client
print(f"Connection Status: {status.decode('ascii')}")

# Sending a value username (min 3 characters) to the server
while True: 
    username = input("Please enter your username (at least 3 characters): ")
    if len(username)>2:
        break
server.sendall(username.encode('ascii'))

# Going to an infinite loop for receiving and printing the messages
while True:
    sockets_list = [sys.stdin, server]
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
    for socks in read_sockets:
        if socks == server:
            data = socks.recv(2048)
            message =data.decode('ascii')
            print (message)
        else:
            message = sys.stdin.readline()
            server.send(message.encode('ascii'))
            #sys.stdout.write("My Message")
            #sys.stdout.write(message)
            sys.stdout.flush()

server.close()
