import socket
import threading

host = "localhost"
port = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Demander le mot de passe
password = input("Entrez le mot de passe pour accéder au chat: ")

# Envoyer le mot de passe au serveur
client_socket.send(password.encode())

# Attendre la réponse du serveur
response = client_socket.recv(1024).decode()

if response == "OK":
    print("Mot de passe correct. Vous pouvez maintenant discuter.\n")
else:
    print("Mot de passe incorrect. La connexion est fermée.")
    client_socket.close()
    exit()

username = input("Entrez votre nom d'utilisateur: ")
client_socket.send(username.encode())

def receive_messages():
    while True:
        message = client_socket.recv(1024).decode()
        print(message)

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    message = input()
    client_socket.send(message.encode())
