import socket
import threading

# Choose nickname
nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))  # Make sure server is using same host/port

# Receive messages from server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8').strip()
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)  # Server messages will be printed as-is
        except:
            print("An error occurred. Disconnecting...")
            client.close()
            break

# Send messages to server
def write():
    while True:
        try:
            msg = input()
            message = f'{nickname}: {msg}'
            client.send(message.encode('utf-8'))
        except:
            break

# Start threads for sending and receiving
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
