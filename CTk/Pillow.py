import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Image Editor")
        self.geometry("800x600")
        self.configure(bg="#333333")

        # Get window dimensions
        self.max_width = 700  # Slightly smaller than window width
        self.max_height = 500 # Leave space for buttons

        self.image = None
        self.image_tk = None

        self.image_label = tk.Label(self, bg="#333333")
        self.image_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.btn_frame = tk.Frame(self, bg="#333333")
        self.btn_frame.grid(row=1, column=0, columnspan=3, pady=10)

        tk.Button(self.btn_frame, text='Load Image',
                command=self.load_image, bg='#555555', fg='black').grid(row=0, column=0, padx=10)
        tk.Button(self.btn_frame, text='Rotate Left',
                command=self.rotate_left, bg='#555555', fg='black').grid(row=0, column=1, padx=10)
        tk.Button(self.btn_frame, text="Rotate Right",
                command=self.rotate_right, bg='#555555', fg='black').grid(row=0, column=2, padx=10)
        
    def resize_image(self, image):
        # Get image size
        width, height = image.size
        
        # Calculate aspect ratio
        aspect = width / height
        
        if width > self.max_width or height > self.max_height:
            if aspect > 1:
                # Image is wider than tall
                new_width = self.max_width
                new_height = int(self.max_width / aspect)
            else:
                # Image is taller than wide
                new_height = self.max_height
                new_width = int(self.max_height * aspect)
                
            return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        return image

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.image = Image.open(file_path)
            self.image = self.resize_image(self.image)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.image_tk)

    def rotate_left(self):
        if self.image:
            def spin():
                self.image = self.image.rotate(-15)
                self.update_image()
                self.update()
                self.after(50, spin)
            spin()
            
    def rotate_right(self):
        if self.image:
            def spin():
                self.image = self.image.rotate(15) 
                self.update_image()
                self.update()
                self.after(50, spin)
            spin()
            
    def update_image(self):
        self.image = self.resize_image(self.image)
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_label.config(image=self.image_tk)
        
if __name__ == "__main__":
    app = ImageEditor()
    app.mainloop()