import socket
import threading


host = "localhost"
port = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((host, port))

server_socket.listen()

clients = []
users = {}

def broadcast_message(sender_socket, message):
    for client_socket in clients:
        if client_socket != sender_socket:
            client_socket.send(message)

def handle_client_connection(client_socket):
    # Demander le nom d'utilisateur du client
    client_socket.send("Entrez votre nom d'utilisateur: ".encode())
    username = client_socket.recv(1024).decode()

    users[client_socket] = username
    clients.append(client_socket)

    welcome_message = f"{username} a rejoint le chat".encode()
    broadcast_message(client_socket, welcome_message)

    while True:
       
        try:
            message = client_socket.recv(1024)
            if message:

                broadcast_message(client_socket, f"{username}: {message}".encode())
            else:
               
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


















