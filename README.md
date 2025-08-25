Python Chat Application: A Deep Dive into Networking
Welcome. This isn't just a simple messaging app; it's a hands-on project built from the ground up to explore and demonstrate the fundamental concepts of network programming in Python. It allows multiple users to connect to a central server and communicate in real-time, all without relying on external services or complex frameworks.

The goal was to move beyond theory and build a tangible application that puts core networking principles into practice.

Features Implemented
Real-Time Group Chat: A central chat room where messages are broadcast to all connected users instantly.

Multi-Client Architecture: The server is built with threading to handle multiple client connections simultaneously and seamlessly.

Private Messaging: Users can send private messages to one another using a /whisper <username> <message> command.

Dynamic User Lists: See who's currently online with the /list command in the CLI client or via an auto-updating list in the GUI client.

Unique Username Validation: The server ensures no two users can have the same name, preventing confusion.

Dual Clients:

A lightweight Command-Line (CLI) client for a pure, terminal-based experience.

A user-friendly Graphical (GUI) client built with Tkinter for a more intuitive chat window.

Core Networking Concepts in Action
This project is a practical demonstration of the following key computer networking concepts:

1. TCP/IP Sockets (socket library)
Sockets are the endpoints of a two-way communication link between two programs running on the network. They can be thought of as the digital equivalent of a telephone.

The Server as the Operator: The server.py script creates a "listening" socket (server_socket.listen()). It functions like a telephone operator waiting for calls on a specific number (the IP address and Port).

The Client Placing a Call: When a client runs, it creates an "active" socket and uses client_socket.connect() to "dial" the server's number.

Establishing a Connection: The server hears the call and uses server_socket.accept() to pick it up, establishing a dedicated, private line between that specific client and the server.

2. The Client-Server Model
This project follows a classic client-server architecture.

The Central Server: The server.py acts as the single source of truth and the central communication hub. It does not initiate conversations; its only job is to manage connections and route messages between the clients. It maintains the state of the chat room, such as the list of connected users and their usernames.

The Clients: The client.py and gui_client.py are the programs the users interact with. They are responsible for sending user input to the server and displaying messages received from the server. They do not know about each other; they only know how to talk to the server.

3. Concurrency with Multithreading (threading library)
A server that can only talk to one client at a time is not very useful. Threading solves this problem.

One Waiter per Table: The main loop in the server waits for new connections. As soon as a new client connects, the server does not handle them directly. Instead, it spawns a new thread (a mini-program) and assigns that thread the job of handling all communication with that specific client.

Parallel Conversations: This is analogous to a restaurant manager greeting new guests and assigning a dedicated waiter to each table. It allows the server to manage many parallel conversations at once, ensuring that a slow or busy client does not block the entire application for everyone else. The client also uses threading to listen for incoming messages and wait for user input simultaneously.

How to Run This Project
Clone the Repository:

git clone https://github.com/satwikapotla/messaging-app.git
cd messaging-app

Start the Server:
Open a terminal or command prompt and run the server. It will start listening for connections.

python server.py

Run a Client:
Open a new, separate terminal and run either the GUI or the CLI client. You can open multiple client windows to simulate a real chat room.

For the Graphical Interface:

python gui_client.py

For the Command-Line Interface:

python client.py

Start Chatting:
Choose a unique username in each client window and start sending messages.

Future Enhancements
Offline Message Storage: Store messages for users who are offline and deliver them upon their next login.

File Transfer: Allow users to send images and other files.

End-to-End Encryption: Implement encryption to ensure messages are secure and can only be read by the sender and recipient.

Persistent User Accounts: Add password authentication and store user accounts in a database like SQLite.