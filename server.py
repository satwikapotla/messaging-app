# server.py
import socket

# --- Configuration ---
# '127.0.0.1' is the standard address for "this computer" (localhost).
# We pick a port number that is likely to be free.
HOST = '127.0.0.1'
PORT = 9090

# 1. Create the main server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Bind the socket to our address and port so it can listen
server_socket.bind((HOST, PORT))

# 3. Start listening for incoming connections
server_socket.listen()
print(f"[*] Server is listening on {HOST}:{PORT}")

# 4. Wait for a client to connect
# Your program will pause here until a client runs and connects.
client_socket, client_address = server_socket.accept()
print(f"[+] Accepted connection from {client_address}")

# 5. Send a simple welcome message to the client
# Data must be sent as bytes, so we .encode() the string.
client_socket.send("Welcome! You have connected to the server.".encode('utf-8'))

# 6. Close the connection
# In this simple version, we close the connection right after sending the message.
client_socket.close()
server_socket.close()