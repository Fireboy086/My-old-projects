import customtkinter as ctk
import random
import string
from tkinter import messagebox

class PasswordGenerator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_variables() 
        self.create_widgets()

    def setup_window(self):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.title("Password Generator")
        self.geometry("400x550")
        self.resizable(False, False)

    def setup_variables(self):
        self.lowercase_var = ctk.BooleanVar(value=True)
        self.uppercase_var = ctk.BooleanVar(value=True) 
        self.digits_var = ctk.BooleanVar(value=True)
        self.special_var = ctk.BooleanVar(value=False)
        self.length_var = ctk.IntVar(value=12)

    def create_widgets(self):
        self.create_title()
        self.create_password_display()
        self.create_options()
        self.create_length_controls()
        self.create_generate_button()
        self.create_copy_button()

    def create_title(self):
        title = ctk.CTkLabel(self, 
            text="Password Generator",
            font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=(20, 10))

    def create_password_display(self):
        frame = ctk.CTkFrame(self)
        frame.pack(padx=20, pady=10, fill="x")
        
        # Label for the password display
        label = ctk.CTkLabel(frame, text="Generated Password:", 
        font=ctk.CTkFont(size=14))
        label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.password_display = ctk.CTkEntry(frame, 
            font=ctk.CTkFont(size=16, family="Courier"),
            height=40)
        self.password_display.pack(padx=10, pady=(0, 10), fill="x")

    def create_options(self):
        frame = ctk.CTkFrame(self)
        frame.pack(padx=20, pady=10, fill="x")
        
        options_label = ctk.CTkLabel(frame, 
            text="Character Types:", 
            font=ctk.CTkFont(size=16, weight="bold"))
        options_label.pack(anchor="w", padx=10, pady=(10, 5))

        options = [
            ("Lowercase (a-z)", self.lowercase_var),
            ("Uppercase (A-Z)", self.uppercase_var), 
            ("Digits (0-9)", self.digits_var),
            ("Special Characters (!@#$%^&*...)", self.special_var)
        ]

        for text, var in options:
            checkbox = ctk.CTkCheckBox(frame, text=text, variable=var)
            checkbox.pack(anchor="w", padx=20, pady=5)

    def create_length_controls(self):
        frame = ctk.CTkFrame(self)
        frame.pack(padx=20, pady=10, fill="x")

        length_label = ctk.CTkLabel(frame,
            text="Password Length:",
            font=ctk.CTkFont(size=16, weight="bold"))
        length_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.length_value_label = ctk.CTkLabel(frame, text=str(self.length_var.get()))
        self.length_value_label.pack(anchor="w", padx=10)

        slider = ctk.CTkSlider(frame,
            from_=4, to=64,
            variable=self.length_var,
            command=self.update_length_label)
        slider.pack(padx=10, pady=10, fill="x")

        min_max = ctk.CTkFrame(frame, fg_color="transparent") 
        min_max.pack(fill="x", padx=10)
        
        ctk.CTkLabel(min_max, text="4").pack(side="left")
        ctk.CTkLabel(min_max, text="64").pack(side="right")

    def create_generate_button(self):
        generate = ctk.CTkButton(self,
            text="Generate",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40,
            command=self.generate_password)
        generate.pack(padx=20, pady=(20, 10), fill="x")

    def create_copy_button(self):
        copy = ctk.CTkButton(self,
            text="Copy",
            font=ctk.CTkFont(size=14),
            height=30,
            command=self.copy_password)
        copy.pack(padx=20, pady=(0, 20), fill="x")

    def update_length_label(self, value):
        self.length_value_label.configure(text=str(int(value)))

    def generate_password(self):
        if not any([self.lowercase_var.get(), self.uppercase_var.get(),
                    self.digits_var.get(), self.special_var.get()]):
            messagebox.showerror("Error", "Please select at least one character type!")
            return

        chars = ""
        if self.lowercase_var.get(): chars += string.ascii_lowercase
        if self.uppercase_var.get(): chars += string.ascii_uppercase
        if self.digits_var.get(): chars += string.digits
        if self.special_var.get(): chars += string.punctuation

        password = ''.join(random.choice(chars) for _ in range(self.length_var.get()))
        
        self.password_display.delete(0, "end")
        self.password_display.insert(0, password)

    def copy_password(self):
        if not self.password_display.get():
            messagebox.showinfo("Info", "Generate a password first!")
            return
            
        self.clipboard_clear()
        self.clipboard_append(self.password_display.get())
        messagebox.showinfo("Success", "Password copied to clipboard!")

if __name__ == "__main__":
    app = PasswordGenerator()
    app.mainloop()