import socket
import threading

# Configuration du serveur
host = "localhost"
port = 5000

# Initialisation de la socket du serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Association de la socket du serveur avec l'adresse et le port
server_socket.bind((host, port))

# Écoute des connexions entrantes
server_socket.listen()

# Liste des clients connectés
clients = []

# Dictionnaire des utilisateurs connectés avec leur socket correspondante
users = {}

# Fonction de diffusion de message à tous les clients connectés
def broadcast_message(sender_socket, message):
    for client in clients:
        if client != sender_socket:
            client.send(message)

# Fonction de gestion de la connexion avec un client
def handle_client_connection(client_socket):
    while True:
        try:
            # Réception du message du client
            message = client_socket.recv(1024)
            if message:
                # Si le client envoie un message, on le diffuse à tous les autres clients
                username = users[client_socket]
                broadcast_message(client_socket, f"{username}: {message}".encode())
            else:
                # Si le client se déconnecte, on supprime ses informations de connexion
                if client_socket in clients:
                    clients.remove(client_socket)
                if client_socket in users:
                    username = users[client_socket]
                    broadcast_message(client_socket, f"{username} a quitté le chat".encode())
                    del users[client_socket]
                client_socket.close()
                break
        except:
            # En cas d'erreur, la connexion est fermée
            if client_socket in clients:
                clients.remove(client_socket)
            if client_socket in users:
                username = users[client_socket]
                broadcast_message(client_socket, f"{username} a quitté le chat".encode())
                del users[client_socket]
            client_socket.close()
            break

# Fonction de gestion des connexions entrantes des clients
def accept_clients():
    while True:
        # Accepter une connexion entrante
        client_socket, client_address = server_socket.accept()

        # Demander au client son nom d'utilisateur
        client_socket.send("Entrez votre nom d'utilisateur: ".encode())
        username = client_socket.recv(1024).decode().strip()

        # Ajouter le client à la liste des clients connectés
        clients.append(client_socket)

        # Ajouter le client et son nom d'utilisateur au dictionnaire des utilisateurs connectés
        users[client_socket] = username

        # Diffuser le message de connexion à tous les autres clients
        broadcast_message(client_socket, f"{username} a rejoint le chat".encode())

        # Créer un thread pour gérer la connexion avec ce client
        thread = threading.Thread(target=handle_client_connection, args=(client_socket,))
        thread.start()

# Démarrer le serveur
print(f"Serveur démarré sur {host}:{port}")
accept_clients()
