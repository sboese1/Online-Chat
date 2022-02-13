import socket
import random
from threading import Thread
from datetime import datetime

host = "127.0.0.1"
port = 5002
separator_token = '<SEP>'

s = socket.socket() # Creates a new socket object
print(f"[*] Connecting to {host}:{port}...")
s.connect((host, port)) # Connects to the remote socket at the given address
print("[+] Connected.")

name = input("Enter your name: ")

def listen_for_messages():
    while True:
        message = s.recv(1024).decode() # Receives data from sockets and decodes it
        print("\n" + message)

t = Thread(target=listen_for_messages) # Creates a Thread object with the object being the function listen_for_messages
t.daemon = True
t.start()

while True:
    to_send = input()
    if to_send.lower() == 'q':
        break
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Gets the current time
    to_send = f"[{date_now}] {name}{separator_token}{to_send}"
    s.send(to_send.encode()) # Sends the encoded message

s.close()
