# gui_client.py
import tkinter as tk
from tkinter import simpledialog, scrolledtext
import socket
import threading

HOST = '127.0.0.1'
PORT = 9090

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat App")
        
        # --- Username Dialog ---
        self.username = simpledialog.askstring("Username", "Please choose your username:", parent=self.root)
        if not self.username: # If user cancels
            self.root.destroy()
            return
            
        # --- GUI Widgets ---
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled')
        self.chat_area.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)
        
        self.user_list = tk.Listbox(self.root, width=20)
        self.user_list.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.Y)

        self.msg_entry = tk.Entry(self.root, width=50)
        self.msg_entry.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.X, expand=True)
        self.msg_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=20, pady=20)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- Network Connection ---
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((HOST, PORT))
        except ConnectionRefusedError:
            self.add_message_to_chat("Connection failed. Is the server running?")
            return

        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message == "USER":
                    self.client_socket.send(self.username.encode('utf-8'))
                    response = self.client_socket.recv(1024).decode('utf-8')
                    if response == "TAKEN":
                        self.add_message_to_chat(f"Username '{self.username}' is taken. Please restart and choose another.")
                        self.client_socket.close()
                        return
                elif message.startswith("USERLIST:"):
                    users = message.split(":")[1].split(',')
                    self.update_user_list(users)
                elif message:
                    self.add_message_to_chat(message)
                else:
                    break
            except:
                self.add_message_to_chat("Connection to server lost.")
                self.client_socket.close()
                break

    def send_message(self, event=None):
        message = self.msg_entry.get()
        if message:
            self.client_socket.send(message.encode('utf-8'))
            self.msg_entry.delete(0, tk.END)

    def add_message_to_chat(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + '\n')
        self.chat_area.yview(tk.END)
        self.chat_area.config(state='disabled')

    def update_user_list(self, users):
        self.user_list.delete(0, tk.END)
        for user in users:
            self.user_list.insert(tk.END, user)

    def on_closing(self):
        self.client_socket.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()