import socket
from threading import Thread

host = '0.0.0.0'
port = 5002
separator_token = '<SEP>'

client_sockets = set()
s = socket.socket() # Creates a new socket object
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Sets the SO_REUSEADDR in the socket to one
s.bind((host, port)) # Binds the socket to the address given
s.listen(5)
print(f'[*] Listening as {host}:{port}')


def listening(cs):
    while True:
        try:
            msg = cs.recv(1024).decode() # Receives data from sockets and decodes it
        except Exception as e:
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)  # If the socket is giving an error, remove it
        else:
            msg = msg.replace(separator_token, ": ")
        for client_socket in client_sockets:
            client_socket.send(msg.encode()) # Send the encoded message

while True:
    client_socket, client_address = s.accept() # Waits for an incoming connection and returns the socket and address
    print(f"[+] {client_address} connected.")
    client_sockets.add(client_socket)

    t = Thread(target=listening, args=(client_socket,)) # Creates a Thread object with the target being the listening function
    t.daemon = True                                     # which takes in the client socket as a parameter
    t.start()


for cs in client_sockets:
    cs.close()

s.close()
