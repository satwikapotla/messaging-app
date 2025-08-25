# client.py
import socket
import threading
import os # We need the 'os' library to properly exit the program

# This function will run in a thread to continuously receive messages
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == "USER":
                username = input("Please choose your username: ")
                client_socket.send(username.encode('utf-8'))
            elif message:
                print(message)
            else:
                # Server has closed the connection
                print("Server disconnected. Shutting down.")
                os._exit(0)
        except:
            print("An error occurred. Disconnecting from server.")
            os._exit(0)

# This function now handles the /quit command
def send_messages(client_socket):
    while True:
        message = input('') # Wait for the user to type something
        if message.lower() == '/quit':
            print("Disconnecting from server.")
            client_socket.close()
            os._exit(0) # Forcefully stops all threads and exits
        client_socket.send(message.encode('utf-8'))

# --- Main Client Logic ---
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect(('127.0.0.1', 9090))
except ConnectionRefusedError:
    print("[!] Connection failed. Is the server running?")
    exit()

receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

send_messages(client_socket)