import socket
import threading

# Configuration du serveur
host = "localhost"
port = 5000

# Création d'un socket pour le serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Lier le socket à l'adresse et au port
server_socket.bind((host, port))

# Attendre les connexions entrantes
server_socket.listen()

# Listes pour stocker les clients et leurs noms d'utilisateur
clients = []
users = {}

# Fonction pour diffuser un message à tous les clients
def broadcast_message(sender_socket, message):
    for client_socket in clients:
        if client_socket != sender_socket:
            client_socket.send(message)

# Fonction pour gérer les connexions des clients
def handle_client_connection(client_socket):
    # Demander le nom d'utilisateur du client
    client_socket.send("Entrez votre nom d'utilisateur: ".encode())
    username = client_socket.recv(1024).decode()

    # Ajouter le client et son nom d'utilisateur aux listes
    users[client_socket] = username
    clients.append(client_socket)

    # Diffuser un message d'accueil à tous les clients
    welcome_message = f"{username} a rejoint le chat".encode()
    broadcast_message(client_socket, welcome_message)

    while True:
        # Attendre les messages du client
        try:
            message = client_socket.recv(1024)
            if message:
                # Diffuser le message à tous les clients
                broadcast_message(client_socket, f"{username}: {message}".encode())
            else:
                # En cas de déconnexion, supprimer le client et son nom d'utilisateur
                if client_socket in clients:
                    clients.remove(client_socket)
                if client_socket in users:
                    username = users[client_socket]
                    broadcast_message(client_socket, f"{username} a quitté le chat".encode())
                    del users[client_socket]
                client_socket.close()
                break
        except:
            # En cas d'erreur, la connexion est fermée proprement
            if client_socket in clients:
                clients.remove(client_socket)
            if client_socket in users:
                username = users[client_socket]
                broadcast_message(client_socket, f"{username} a quitté le chat".encode())
                del users[client_socket]
            client_socket.close()
            break

# Liste pour stocker les threads de connexion client
threads = []

try:
    while True:
        # Attendre une connexion entrante
        client_socket, address = server_socket.accept()
        print(f"Connexion acceptée de {address[0]}:{address[1]}")

        # Créer un thread pour gérer la connexion client
        thread = threading.Thread(target=handle_client_connection, args=(client_socket,))
        threads.append(thread)
        thread.start()

except KeyboardInterrupt:
    print("Arrêt demandé, fermeture des connexions...")

    # Fermer toutes les connexions clients
    for client_socket in clients:
        client_socket.close()

    # Attendre que tous les threads se terminent
    for thread in threads:
        thread.join()

    # Fermer le socket serveur
    server_socket.close()


















