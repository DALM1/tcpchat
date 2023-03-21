import socket
import threading

# Configuration du client
host = "localhost"
port = 5000

# Connexion au serveur
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Demande de nom d'utilisateur
username = input("Entrez votre nom d'utilisateur: ")

# Envoi du nom d'utilisateur au serveur
client_socket.send(username.encode())

# Fonction pour recevoir et afficher les messages des autres utilisateurs
def receive_messages():
    while True:
        message = client_socket.recv(1024).decode()
        print(message)

# Création d'un thread pour recevoir les messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Boucle principale du client pour envoyer des messages
while True:
    message = input()
    client_socket.send(message.encode())
