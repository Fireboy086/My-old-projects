import customtkinter as ctk

class ClickerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Simple Clicker")
        self.geometry("500x500")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        
        self.counter = 0
        
        self.label = ctk.CTkLabel(
            self, 
            text=str(self.counter),
            font=("Arial", 150),
            text_color="#FE2621"
        )
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.button = ctk.CTkButton(
            self,
            text="CLICK ME",
            font=("Arial", 24, "bold"),
            command=self.increment_counter,
            fg_color="#05445E",
            hover_color="#189AB4",
            height=60
        )
        self.button.grid(row=1, column=0, padx=50, pady=30, sticky="ew")
    
    def increment_counter(self):
        self.counter += 1
        self.label.configure(text=str(self.counter))
        if self.counter >= 10:
            # self.destroy()
            congrats_window = ctk.CTk()
            congrats_window.title("Congrats")
            congrats_window.geometry("300x200")
            
            canvas = ctk.CTkCanvas(congrats_window, bg="#242424")
            canvas.pack(fill="both", expand=True)
            
            congrats_label = ctk.CTkLabel(canvas, text="Congrats", font=("Arial", 24))
            congrats_label.pack(pady=20)
            
            fuck_you_label = ctk.CTkLabel(canvas, text="fuck you", font=("Arial", 8), text_color="#303030")
            fuck_you_label.place(x=100, y=1000)
            
            congrats_window.after(10000, congrats_window.destroy)
            congrats_window.mainloop()
        elif self.counter >= 10000:
            self.label.configure(font=("Arial", 80))
        elif self.counter >= 1000:
            self.label.configure(font=("Arial", 100))
        elif self.counter >= 100:
            self.label.configure(font=("Arial", 120))
        

if __name__ == "__main__":
    app = ClickerApp()
    app.mainloop()