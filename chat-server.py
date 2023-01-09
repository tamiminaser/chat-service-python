import socket
import _thread

HOST = "" # If HOST become a empty string, then the server accepts requests from any ip.
PORT = 5000 # Port to listen on
threadCount = 0
listOfClients = []

def multi_threaded_client(conn, addr):
    conn.sendall(str.encode("Successful connection."))

    # Recieving the username
    data = conn.recv(1024)
    username = data.decode('ascii')

    # Going to an infinite loop to receive and publish messages
    while True:
        try: 
            data = conn.recv(1024)
            if not data:
                break
            
            msg = username+": "+data.decode('ascii')
            
            # Logging and printing information on the server side only.
            print(f"[{addr[0]}:{addr[1]}] {msg}")

            # Broadcasting the message to all clients
            for client in listOfClients:
                if client!=conn:
                    try:
                        client.send(msg.encode('ascii'))
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)
        
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INTET indicates that the address family is IPv4
# SOCK_STREAM is the socket type for TCP
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT)) # Associtate socket object s with specific interface and port number
s.listen()

while True:
    conn, addr = s.accept() # conn is a new object to talk to client. addr is the address of the connected client.
    listOfClients.append(conn)
    print('Connected to: ' + addr[0] + ':' + str(addr[1]))
    _thread.start_new_thread(multi_threaded_client, (conn, addr))
    threadCount += 1
    print('Thread Number: ' + str(threadCount))

s.close()