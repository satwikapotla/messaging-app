import socket

# --- Configuration ---
# This MUST match the server's HOST and PORT exactly.
HOST = '127.0.0.1'
PORT = 9090

# 1. Create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Connect to the server
try:
    client_socket.connect((HOST, PORT))
    print(f"[*] Successfully connected to the server.")

    # 3. Receive the message from the server
    # 1024 is the buffer size (how much data to get at once).
    # We must .decode() the bytes back into a string to read it.
    message = client_socket.recv(1024).decode('utf-8')
    print(f"Server says: {message}")

except ConnectionRefusedError:
    print("[!] Connection failed. Make sure the server is running first.")

finally:
    # 4. Close the connection
    client_socket.close()