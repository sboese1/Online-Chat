import socket
from threading import Thread

host = '0.0.0.0'
port = 5002
separator_token = '<SEP>'

client_sockets = set()
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)
print(f'[*] Listening as {host}:{port}')


def listening(cs):
    while True:
        try:
            msg = cs.recv(1024).decode()
        except Exception as e:
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            msg = msg.replace(separator_token, ": ")
        for client_socket in client_sockets:
            client_socket.send(msg.encode())

while True:
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    client_sockets.add(client_socket)

    t = Thread(target=listening, args=(client_socket,))
    t.daemon = True
    t.start()


for cs in client_sockets:
    cs.close()
s.close()