import socket
import threading

ip = 'localhost'
port = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, port))


def listen_for_client():
    while True:
        message = client.recv(1024).decode()
        print(message)


a1 = threading.Thread(target=listen_for_client)
a1.start()

while True:
    a = input()
    client.send(a.encode())
