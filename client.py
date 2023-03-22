import socket
import threading

host = "localhost"
port = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

username = input("Entrez votre nom d'utilisateur: ")
client_socket.send(username.encode())
print("\n")



def receive_messages():
    while True:
        message = client_socket.recv(1024).decode()
        print(message)

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    message = input("> ")
    client_socket.send(message.encode())
    print("\n")

if message.lower() == "/quit":
    break