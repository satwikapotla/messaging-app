# client.py
import socket
import threading
import os

def receive_messages(client_socket, username_accepted_event):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == "USER":
                while True:
                    username = input("Please choose your username: ")
                    client_socket.send(username.encode('utf-8'))
                    response = client_socket.recv(1024).decode('utf-8')
                    if response == "OK":
                        # CHANGE 1: The light turns green. Username is set, so we can proceed.
                        username_accepted_event.set()
                        break
                    else: # Response was "TAKEN"
                        print("Username is already taken. Please choose another.")
            elif message:
                print(message)
            else:
                print("Server disconnected. Shutting down.")
                os._exit(0)
        except:
            print("An error occurred. Disconnecting.")
            os._exit(0)

def send_messages(client_socket, username_accepted_event):
    # CHANGE 2: Wait for the green light before starting the message loop.
    username_accepted_event.wait() 
    
    print("You can now start sending messages!")
    while True:
        message = input('')
        if message.lower() == '/quit':
            print("Disconnecting from server.")
            client_socket.close()
            os._exit(0)
        client_socket.send(message.encode('utf-8'))

# --- Main Client Logic ---
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect(('127.0.0.1', 9090))
except ConnectionRefusedError:
    print("[!] Connection failed. Is the server running?")
    exit()

# CHANGE 3: Create the "traffic light" event. It starts as red.
username_accepted = threading.Event()

receive_thread = threading.Thread(target=receive_messages, args=(client_socket, username_accepted))
receive_thread.start()

# We can now start the send_messages in its own thread too for cleaner structure
send_thread = threading.Thread(target=send_messages, args=(client_socket, username_accepted))
send_thread.start()