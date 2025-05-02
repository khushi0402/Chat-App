import socket
import threading

# Server config
HOST = '127.0.0.1'
PORT = 12345

# Create socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

# Broadcast messages to all clients
def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except:
            clients.remove(client)
            client.close()

# Handle individual client
def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8').strip()  # Remove extra spaces/newlines
            if message:
                broadcast(f"{message}\n")  # Add newline for readability
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!\n')  # Add newline
            nicknames.remove(nickname)
            break

# Accept clients
def receive():
    print(f"Server running on {HOST}:{PORT}...")
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode('utf-8'))  # Request nickname
        nickname = client.recv(1024).decode('utf-8').strip()  # Clean up any extra spaces
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname is {nickname}')
        broadcast(f'{nickname} joined the chat!\n')  # Notify others
        client.send('Connected to the server!\n'.encode('utf-8'))  # Welcome message

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
