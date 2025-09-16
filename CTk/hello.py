import customtkinter as ctk

window = ctk.CTk()

window.title("Hello")

window.geometry("400x400")

text_field = ctk.CTkTextbox(window, width=380, height=280)
text_field.pack(pady=10)

text_entry = ctk.CTkEntry(window, width=380)
text_entry.pack(pady=10)

button = ctk.CTkButton(window, width=380, height=100, text="Click me")
button.pack(pady=10)

window.mainloop()
