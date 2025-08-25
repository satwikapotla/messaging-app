# server.py
import socket
import threading

HOST = '127.0.0.1'
PORT = 9090

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print(f"[*] Server is live and listening on {HOST}:{PORT}")

# Lists to store the socket objects and usernames of connected clients
clients = []
usernames = []

# This function sends a message to all connected clients except the sender
def broadcast(message, _sender_socket):
    for client_socket in clients:
        if client_socket != _sender_socket:
            try:
                client_socket.send(message)
            except:
                # If sending fails, the client has likely disconnected
                remove_client(client_socket)

# This function removes a client when they disconnect
def remove_client(client_socket):
    if client_socket in clients:
        index = clients.index(client_socket)
        clients.remove(client_socket)
        username = usernames[index]
        usernames.remove(username)
        print(f"[-] {username} has disconnected.")
        broadcast(f"{username} has left the chat.".encode('utf-8'), client_socket)

# This function handles a single client's connection
def handle_client(client_socket):
    try:
        # Ask the client for their username
        client_socket.send("USER".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8')
        usernames.append(username)
        clients.append(client_socket)
        
        print(f"[+] {username} has connected.")
        broadcast(f"{username} has joined the chat!".encode('utf-8'), client_socket)
        client_socket.send("Connected to the server!".encode('utf-8'))

        # Continuously listen for messages from this client
        while True:
            message = client_socket.recv(1024)
            if message:
                broadcast(f"<{username}> {message.decode('utf-8')}".encode('utf-8'), client_socket)
            else:
                # An empty message means the client disconnected
                remove_client(client_socket)
                break
    except:
        remove_client(client_socket)

# --- Main Server Loop ---
# This loop continuously waits for new clients to connect
while True:
    client_socket, address = server_socket.accept()
    # Create a new thread for each client that connects
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()