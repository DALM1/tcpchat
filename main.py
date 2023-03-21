import socket
import threading

class Client:
    def __init__(self, server, name):
        self.server = server
        self.name = name
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server.host, server.port))
        self.socket.sendall(f"CONNECT {self.name}".encode())
        self.is_running = True

        self.disconnect_timer = threading.Timer(10.0, self.disconnect)
        self.disconnect_timer.start()

    def send(self, message):
        self.socket.sendall(f"MESSAGE {self.name}: {message}".encode())
        self.disconnect_timer.cancel()
        self.disconnect_timer = threading.Timer(10.0, self.disconnect)
        self.disconnect_timer.start()

    def disconnect(self):
        self.is_running = False
        self.socket.sendall(f"DISCONNECT {self.name}".encode())
        self.socket.close()

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.clients = []

    def start(self):
        self.socket.listen()
        while True:
            conn, addr = self.socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(conn,))
            client_thread.start()

    def handle_client(self, conn):
        name = None
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode()
            if message.startswith("CONNECT"):
                name = message.split()[1]
                self.clients.append((name, conn))
                print(f"{name} connected")
            elif message.startswith("MESSAGE"):
                if name is None:
                    conn.sendall("ERROR You must connect first".encode())
                else:
                    for client_name, client_conn in self.clients:
                        if client_name != name:
                            client_conn.sendall(message.encode())
            elif message.startswith("DISCONNECT"):
                if name is not None:
                    self.clients.remove((name, conn))
                    print(f"{name} disconnected")
                    break
            else:
                conn.sendall("ERROR Invalid command".encode())
        conn.close()

if __name__ == "__main__":
    server = Server("localhost", 8000)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    client1 = Client(server, "Alice")
    client2 = Client(server, "Bob")

    client1.send("Hello, Bob!")
    client2.send("Hi, Alice!")

    # Wait for the clients to finish
    while client1.is_running or client2.is_running:
        pass
