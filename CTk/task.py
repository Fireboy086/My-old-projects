
from customtkinter import *

class MainWindow(CTk):
    # initialize the window
    def __init__(self):
        super().__init__()
        self.title("CustomTkinter Example")  # set title
        self.geometry("400x300")  # set size

        # menu frame
        self.menu_frame = CTkFrame(self, width=30, height=300)
        self.menu_frame.pack_propagate(False)
        self.menu_frame.place(x=0, y=0)

        # menu state variables
        self.is_show_menu = False
        self.speed_animate_menu = -5

        # toggle menu button
        self.btn = CTkButton(self, text='▶️', command=self.toggle_show_menu, width=30, height=30)
        self.btn.place(x=0, y=0)

        # chat text box
        self.chat_field = CTkTextbox(self, font=("Arial", 12, "bold"))
        self.chat_field.place(x=0, y=0)

        # message entry field
        self.message_entry = CTkEntry(self, placeholder_text="Start yappin'  :", height=40)
        self.message_entry.place(x=0, y=0)

        # send button
        self.send_button = CTkButton(self, text='➡', width=50, height=40)
        self.send_button.place(x=0, y=0)

        self.adaptive_ui()  # start adaptive UI

    # toggle the menu visibility
    def toggle_show_menu(self):
        if self.is_show_menu:
            self.is_show_menu = False
            self.speed_animate_menu *= -1
            self.btn.configure(text='▶️')  # update button text
            self.show_menu()
        else:
            self.is_show_menu = True
            self.speed_animate_menu *= -1
            self.btn.configure(text='◀️')  # update button text
            self.show_menu()
            # add name label and entry
            self.label = CTkLabel(self.menu_frame, text='Імʼя')
            self.label.pack(pady=30)
            self.entry = CTkEntry(self.menu_frame)
            self.entry.pack()

    # animate showing/hiding the menu
    def show_menu(self):
        self.menu_frame.configure(width=self.menu_frame.winfo_width() + self.speed_animate_menu)
        if self.menu_frame.winfo_width() <= 200 and self.is_show_menu:
            self.after(10, self.show_menu)
        elif not self.is_show_menu and self.menu_frame.winfo_width() > 30:
            self.after(10, self.show_menu)
            if hasattr(self, 'label') and hasattr(self, 'entry'):
                self.label.destroy()
                self.entry.destroy()

    # update the UI layout
    def adaptive_ui(self):
        self.menu_frame.configure(height=self.winfo_height())
        self.chat_field.place(x=self.menu_frame.winfo_width())
        self.chat_field.configure(
            width=self.winfo_width() - self.menu_frame.winfo_width(),
            height=self.winfo_height() - 40
        )
        self.send_button.place(
            x=self.winfo_width() - 50,
            y=self.winfo_height() - 40
        )
        self.message_entry.place(
            x=self.menu_frame.winfo_width(),
            y=self.send_button.winfo_y()
        )
        self.message_entry.configure(
            width=self.winfo_width() - self.menu_frame.winfo_width() - self.send_button.winfo_width()
        )

        self.after(50, self.adaptive_ui)  # keep UI adaptive i guess, i dont know

# create and run the window
window = MainWindow()
window.mainloop()