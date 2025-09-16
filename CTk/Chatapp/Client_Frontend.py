# Import required libraries
import customtkinter as ctk
import threading
from Client_Backend import Client
from datetime import datetime
import socket

class ChatApp:
    def __init__(self):
        # Initialize client connection
        self.client = Client()
        
        # Set up main window
        self.window = ctk.CTk()
        self.window.title("Chat App 💬")
        self.window.geometry("800x600")
        
        # Create top bar frame
        self.top_bar = ctk.CTkFrame(self.window, height=40)
        self.top_bar.pack(fill="x", padx=10, pady=5)
        
        # Add settings button to top bar
        self.settings_btn = ctk.CTkButton(self.top_bar, text="⚙️", width=30, command=self.toggle_options)
        self.settings_btn.pack(side="left", padx=5)
        
        # Add time display to top bar
        self.time_label = ctk.CTkLabel(self.top_bar, text="")
        self.time_label.pack(side="right", padx=5)
        self.update_time()
        
        # Create main content area
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Add chat display area
        self.chat_frame = ctk.CTkTextbox(self.main_frame, width=580, height=400)
        self.chat_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.chat_frame.configure(state="disabled")
        
        # Create message input area
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.pack(fill="x", padx=10, pady=5)
        
        # Add message entry field
        self.msg_entry = ctk.CTkEntry(self.input_frame, width=580, placeholder_text="Type your message...")
        self.msg_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.msg_entry.bind("<Return>", lambda e: self.send_message())
        
        # Add send button
        self.send_btn = ctk.CTkButton(self.input_frame, text="Send", width=80, command=self.send_message)
        self.send_btn.pack(side="right")
        
        # Create options frame at the bottom
        self.options_frame = ctk.CTkFrame(self.window)
        self.options_visible = False
        
        # Add options content
        self.options_label = ctk.CTkLabel(self.options_frame, text="Options", font=("Arial", 20))
        self.options_label.pack(pady=20)
        
        # Appearance Section
        self.appearance_frame = ctk.CTkFrame(self.options_frame)
        self.appearance_frame.pack(fill="x", padx=10, pady=5)
        
        self.appearance_label = ctk.CTkLabel(self.appearance_frame, text="Appearance", font=("Arial", 14))
        self.appearance_label.pack(padx=5)
        
        self.theme_switch = ctk.CTkSwitch(self.appearance_frame, text="Dark Mode", command=self.toggle_theme)
        self.theme_switch.select()  # Turn switch on by default
        self.theme_switch.pack(padx=5)
        
        # User Settings Section
        self.user_frame = ctk.CTkFrame(self.options_frame)
        self.user_frame.pack(fill="x", padx=10, pady=5)
        
        self.user_label = ctk.CTkLabel(self.user_frame, text="User Settings", font=("Arial", 14))
        self.user_label.pack(padx=5)
        
        self.username_btn = ctk.CTkButton(self.user_frame, text="Change Username", command=self.change_username)
        self.username_btn.pack(padx=5)
        
        # Initialize client connection
        self.start_client()
        
        # Start main application loop
        self.window.mainloop()
    
    def update_time(self):
        # Update time display every second
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=current_time)
        self.window.after(1000, self.update_time)
    
    def toggle_options(self):
        # Show/hide options at the bottom
        if self.options_visible:
            self.options_frame.pack_forget()
            self.main_frame.configure(height=600)
        else:
            self.options_frame.pack(side="bottom", fill="x", padx=10, pady=5)
            self.main_frame.configure(height=500)
        self.options_visible = not self.options_visible
    
    def toggle_theme(self):
        # Switch between light/dark themes
        current_theme = ctk.get_appearance_mode()
        new_theme = "Light" if current_theme == "Dark" else "Dark"
        ctk.set_appearance_mode(new_theme)
    
    def change_username(self):
        # Change username dialog
        new_username = ctk.CTkInputDialog(title="Change Username", text="Enter new username:").get_input()
        if new_username:
            self.client.nickname = new_username
            self.update_chat(f"[SYSTEM] Username changed to {new_username}")
    
        
    def start_client(self):
        # Get user nickname and start client
        while True:
            nickname = ctk.CTkInputDialog(title="Nickname", text="Choose your nickname:").get_input()
            if nickname:
                break
            ctk.CTkMessagebox(title="Error", message="Nickname cannot be empty!", icon="warning")
        self.client.nickname = nickname
        # Set socket timeout for better disconnect handling
        self.client.client.settimeout(1.0)
        # Start message receiving thread
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()
        
    def receive_messages(self):
        while True:
            try:
                message = self.client.client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client.client.send(self.client.nickname.encode('utf-8'))
                else:
                    # Use after method to safely update UI from a thread
                    self.window.after(0, self.update_chat, message)
            except (socket.timeout, OSError):
                continue  # Timeout, just try again
            except Exception as e:
                self.window.after(0, self.update_chat, f"[SYSTEM] Disconnected from server. ({e})")
                break
                
    def update_chat(self, message):
        # Safe method to update chat from main thread
        self.chat_frame.configure(state="normal")
        self.chat_frame.insert("end", message + "\n")
        self.chat_frame.configure(state="disabled")
        self.chat_frame.see("end")
        
    def send_message(self):
        # Send message to server
        message = self.msg_entry.get()
        if message:
            full_message = f'[{self.client.nickname}]: {message}'
            try:
                self.client.client.send(full_message.encode('utf-8'))
            except Exception as e:
                self.update_chat(f"[SYSTEM] Failed to send message: {e}")
            self.msg_entry.delete(0, "end")

if __name__ == "__main__":
    app = ChatApp()
