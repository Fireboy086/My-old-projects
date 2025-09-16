import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Chess Board")
root.geometry("600x600")

board_frame = ctk.CTkFrame(root, fg_color="#AAAAAA")
board_frame.pack(expand=True, fill="both", padx=20, pady=20)

ROWS, COLS = 8, 8
BUTTON_SIZE = 60

for row in range(ROWS):
    for col in range(COLS):
        if (row + col) % 2 == 0:
            button_color = "white"
            text_color = "black"
        else:
            button_color = "black"
            text_color = "white"
        
        button = ctk.CTkButton(
            board_frame,
            text="",
            width=BUTTON_SIZE,
            height=BUTTON_SIZE,
            fg_color=button_color,
            text_color=text_color,
            corner_radius=5,
        )
        
        button.grid(row=row, column=col)

for i in range(ROWS):
    board_frame.grid_rowconfigure(i, weight=1)
    board_frame.grid_columnconfigure(i, weight=1)

root.mainloop() 