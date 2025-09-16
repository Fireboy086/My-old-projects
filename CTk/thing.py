import customtkinter as ctk
import math
from typing import Optional

class ChatMessage:
    def __init__(self, username: str, message: str):
        self.username = username
        self.message = message
        self.timestamp = None  # Will be set when sending to server

class ChatInterface(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("EGG")
        self.geometry("800x600")
        self.attributes('-topmost', True)
        self.center_window()
        
        # Animation variables
        self.time_frame = 0
        self.options_visible = False
        self.options_pos = -300
        
        # Create main container with black background
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True)
        
        # Create top bar
        self.create_top_bar()
        
        # Create chat area first (so it's behind)
        self.create_chat_area()
        
        # Create options panel last (so it's on top)
        self.create_options_panel()
        
        # Create input area
        self.create_input_area()
        
        self.continuous_loop()
        
    def create_top_bar(self):
        self.top_bar = ctk.CTkFrame(self.main_container, height=50)
        self.top_bar.pack(fill="x", padx=5, pady=5)
        
        self.options_button = ctk.CTkButton(
            self.top_bar, 
            text="⚙︎",
            width=40,
            command=self.toggle_options
        )
        self.options_button.pack(side="left", padx=5)
        
    def create_options_panel(self):
        self.options_panel = ctk.CTkFrame(self.main_container, width=300)
        self.options_panel.pack_propagate(False)
        
        # Username input
        self.username_label = ctk.CTkLabel(self.options_panel, text="Your Username")
        self.username_label.pack(pady=5, padx=5, fill="x")
        
        self.username_input = ctk.CTkEntry(self.options_panel, placeholder_text="Enter username")
        self.username_input.pack(pady=5, padx=5, fill="x")
        self.username_input.bind("<KeyRelease>", lambda e: self.check_username())
        
        # Theme selector
        self.theme_label = ctk.CTkLabel(self.options_panel, text="Theme")
        self.theme_label.pack(pady=5, padx=5, fill="x")
        
        self.theme_menu = ctk.CTkOptionMenu(
            self.options_panel,
            values=["Dark theme", "Light theme"],
            command=self.change_theme
        )
        self.theme_menu.pack(pady=5, padx=5, fill="x")
        
        self.options_panel.place(x=-300, y=60)
        
    def create_chat_area(self):
        self.chat_container = ctk.CTkFrame(self.main_container)
        self.chat_container.pack(fill="both", expand=True, padx=5, pady=(60, 5))
        
        self.chat_area = ctk.CTkTextbox(self.chat_container, wrap="word")
        self.chat_area.pack(fill="both", expand=True)
        self.chat_area.configure(state="disabled")
        
    def create_input_area(self):
        self.input_frame = ctk.CTkFrame(self.main_container, height=50)
        self.input_frame.pack(fill="x", padx=5, pady=5)
        
        self.message_input = ctk.CTkEntry(self.input_frame, placeholder_text="Type your message...")
        self.message_input.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.message_input.bind("<Return>", lambda e: self.send_message())
        self.message_input.configure(state="disabled")  # Initially disabled
        
        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="Send",
            width=100,
            command=self.send_message
        )
        self.send_button.pack(side="right")
        self.send_button.configure(state="disabled")  # Initially disabled
        
    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (800/2)
        y = (screen_height/2) - (600/2)
        self.geometry(f"+{int(x)}+{int(y)}")
        
    def continuous_loop(self):
        if not self.options_visible and self.options_pos >= -300:
            move_amount = math.ceil((self.options_pos)/10)
            self.options_pos += move_amount if move_amount > 0 else move_amount - 1
        elif self.options_visible and self.options_pos <= 0:
            move_amount = math.floor((self.options_pos-0)/10)
            self.options_pos -= move_amount
            
        self.options_panel.place(x=self.options_pos, y=60)
        self.options_panel.lift()  # Keep options on top
        
        self.time_frame += 0.01
        self.after(5, self.continuous_loop)
        
    def toggle_options(self):
        self.options_visible = not self.options_visible
        
    def send_message(self):
        message = self.message_input.get().strip()
        username = self.username_input.get().strip()
        
        if not message or not username:
            return
            
        # Create message object (ready for socket integration)
        chat_message = ChatMessage(username, message)
        
        # Display message locally (will be replaced with socket logic)
        self.display_message(chat_message)
        
        # Clear input
        self.message_input.delete(0, "end")
        
    def display_message(self, chat_message: ChatMessage):
        self.chat_area.configure(state="normal")
        self.chat_area.insert("end", f"{chat_message.username}: {chat_message.message}\n")
        self.chat_area.configure(state="disabled")
        self.chat_area.see("end")
        
    def change_theme(self, value):
        if value == "Dark theme":
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")
            
    def check_username(self):
        username = self.username_input.get().strip()
        if username:
            self.message_input.configure(state="normal")
            self.send_button.configure(state="normal")
        else:
            self.message_input.configure(state="disabled")
            self.send_button.configure(state="disabled")

if __name__ == "__main__":
    app = ChatInterface()
    app.mainloop()