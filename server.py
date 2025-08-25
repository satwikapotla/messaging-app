# server.py
import socket
import threading

HOST = '127.0.0.1'
PORT = 9090

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print(f"[*] Server is live and listening on {HOST}:{PORT}")

clients = []
usernames = []

def broadcast(message, _sender_socket):
    for client_socket in clients:
        if client_socket != _sender_socket:
            try:
                client_socket.send(message)
            except:
                remove_client(client_socket)

def remove_client(client_socket):
    if client_socket in clients:
        index = clients.index(client_socket)
        clients.remove(client_socket)
        username = usernames[index]
        usernames.remove(username)
        print(f"[-] {username} has disconnected.")
        broadcast(f"{username} has left the chat.".encode('utf-8'), client_socket)

def handle_client(client_socket):
    try:
        # --- MODIFIED: USERNAME HANDLING LOOP ---
        while True:
            client_socket.send("USER".encode('utf-8'))
            username = client_socket.recv(1024).decode('utf-8')
            if username not in usernames:
                client_socket.send("OK".encode('utf-8')) # Signal that the username is accepted
                break
            else:
                client_socket.send("TAKEN".encode('utf-8')) # Signal that the username is taken
        
        usernames.append(username)
        clients.append(client_socket)
        
        print(f"[+] {username} has connected.")
        broadcast(f"{username} has joined the chat!".encode('utf-8'), client_socket)
        client_socket.send("Connected to the server! Type /list to see online users.".encode('utf-8'))

        while True:
            message_str = client_socket.recv(1024).decode('utf-8')
            if message_str:
                if message_str.lower() == '/list':
                    # --- NEW: /list COMMAND LOGIC ---
                    online_users = ", ".join(usernames)
                    list_message = f"Online users: {online_users}".encode('utf-8')
                    client_socket.send(list_message)
                elif message_str.startswith('/whisper'):
                    # (Whisper logic remains the same)
                    try:
                        parts = message_str.split(' ', 2)
                        recipient_username, private_message = parts[1], parts[2]
                        if recipient_username in usernames:
                            recipient_index = usernames.index(recipient_username)
                            recipient_socket = clients[recipient_index]
                            final_message = f"(whisper from {username}): {private_message}".encode('utf-8')
                            recipient_socket.send(final_message)
                            client_socket.send(f"You whispered to {recipient_username}: {private_message}".encode('utf-8'))
                        else:
                            client_socket.send(f"Error: User '{recipient_username}' not found.".encode('utf-8'))
                    except IndexError:
                        client_socket.send("Error: Invalid whisper format.".encode('utf-8'))
                else:
                    broadcast(f"<{username}> {message_str}".encode('utf-8'), client_socket)
            else:
                remove_client(client_socket)
                break
    except:
        remove_client(client_socket)

while True:
    client_socket, address = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()