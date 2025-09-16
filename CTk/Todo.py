import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import sqlite3
import os

class TodoApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Premium Todo")
        self.root.geometry("800x600")
        
        # Modern theme settings
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize database
        self.db_path = "OMG.db"
        self.init_db()
        
        # Initialize data
        self.tasks = []
        self.categories = ["Work", "Personal", "Shopping", "Other"]
        self.load_tasks()
        
        # Create UI
        self.create_widgets()
        
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tasks table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
        ''')
        
        conn.commit()
        conn.close()
        
    def create_widgets(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left sidebar
        self.sidebar = ctk.CTkFrame(self.main_frame, width=200)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        
        # Category selector
        self.category_label = ctk.CTkLabel(self.sidebar, text="Categories", font=("Arial", 16, "bold"))
        self.category_label.pack(pady=10)
        
        self.category_var = ctk.StringVar(value="All")
        for category in ["All"] + self.categories:
            ctk.CTkRadioButton(
                self.sidebar,
                text=category,
                variable=self.category_var,
                value=category,
                command=self.filter_tasks
            ).pack(pady=5)
        
        # Main content area
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Task input area
        self.input_frame = ctk.CTkFrame(self.content_frame)
        self.input_frame.pack(fill="x", pady=10)
        
        self.task_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Enter a task...",
            width=400,
            height=40,
            font=("Arial", 14)
        )
        self.task_entry.pack(side="left", padx=10)
        
        self.category_combo = ctk.CTkComboBox(
            self.input_frame,
            values=self.categories,
            width=150,
            height=40
        )
        self.category_combo.pack(side="left", padx=10)
        
        self.add_button = ctk.CTkButton(
            self.input_frame,
            text="Add Task",
            command=self.add_task,
            width=100,
            height=40,
            font=("Arial", 14, "bold")
        )
        self.add_button.pack(side="left", padx=10)
        
        # Tasks list
        self.tasks_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            width=500,
            height=400
        )
        self.tasks_frame.pack(fill="both", expand=True, pady=10)
        
        # Stats frame
        self.stats_frame = ctk.CTkFrame(self.content_frame)
        self.stats_frame.pack(fill="x", pady=10)
        
        self.stats_label = ctk.CTkLabel(
            self.stats_frame,
            text="Tasks: 0 | Completed: 0",
            font=("Arial", 12)
        )
        self.stats_label.pack()
        
    def add_task(self):
        task_text = self.task_entry.get().strip()
        category = self.category_combo.get()
        
        if task_text:
            # Save to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (text, category, date, completed) VALUES (?, ?, ?, ?)",
                (task_text, category, datetime.now().strftime("%Y-%m-%d"), 0)
            )
            task_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Create UI elements
            task_frame = ctk.CTkFrame(self.tasks_frame)
            task_frame.pack(fill="x", pady=5, padx=5)
            
            var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(
                task_frame,
                text="",
                variable=var,
                command=lambda: self.toggle_task(task_frame, var, task_id)
            )
            checkbox.pack(side="left", padx=10)
            
            task_label = ctk.CTkLabel(
                task_frame,
                text=f"{task_text} ({category})",
                width=300,
                font=("Arial", 14)
            )
            task_label.pack(side="left", padx=10)
            
            date_label = ctk.CTkLabel(
                task_frame,
                text=datetime.now().strftime("%Y-%m-%d"),
                width=100,
                font=("Arial", 12)
            )
            date_label.pack(side="left", padx=10)
            
            delete_button = ctk.CTkButton(
                task_frame,
                text="🗑️",
                width=40,
                command=lambda: self.delete_task(task_frame, task_id)
            )
            delete_button.pack(side="right", padx=10)
            
            self.tasks.append((task_frame, task_id))
            self.update_stats()
            self.task_entry.delete(0, "end")
        else:
            messagebox.showwarning("Warning", "Please enter a task!")
    
    def toggle_task(self, task_frame, var, task_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET completed = ? WHERE id = ?",
            (1 if var.get() else 0, task_id)
        )
        conn.commit()
        conn.close()
        self.update_stats()
    
    def delete_task(self, task_frame, task_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        
        for task, tid in self.tasks:
            if task == task_frame:
                self.tasks.remove((task, tid))
                task_frame.destroy()
                break
        
        self.update_stats()
    
    def filter_tasks(self):
        category = self.category_var.get()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if category == "All":
            cursor.execute("SELECT * FROM tasks")
        else:
            cursor.execute("SELECT * FROM tasks WHERE category = ?", (category,))
        
        tasks = cursor.fetchall()
        conn.close()
        
        # Hide all tasks first
        for task_frame, _ in self.tasks:
            task_frame.pack_forget()
        
        # Show filtered tasks
        for task_frame, task_id in self.tasks:
            for task in tasks:
                if task[0] == task_id:
                    task_frame.pack(fill="x", pady=5, padx=5)
                    break
    
    def update_stats(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tasks")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE completed = 1")
        completed = cursor.fetchone()[0]
        conn.close()
        
        self.stats_label.configure(text=f"Tasks: {total} | Completed: {completed}")
    
    def load_tasks(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        conn.close()
        
        for task in tasks:
            self.add_saved_task(task)
    
    def add_saved_task(self, task_data):
        task_id, text, category, date, completed = task_data
        
        task_frame = ctk.CTkFrame(self.tasks_frame)
        task_frame.pack(fill="x", pady=5, padx=5)
        
        var = ctk.BooleanVar(value=bool(completed))
        checkbox = ctk.CTkCheckBox(
            task_frame,
            text="",
            variable=var,
            command=lambda: self.toggle_task(task_frame, var, task_id)
        )
        checkbox.pack(side="left", padx=10)
        
        task_label = ctk.CTkLabel(
            task_frame,
            text=f"{text} ({category})",
            width=300,
            font=("Arial", 14)
        )
        task_label.pack(side="left", padx=10)
        
        date_label = ctk.CTkLabel(
            task_frame,
            text=date,
            width=100,
            font=("Arial", 12)
        )
        date_label.pack(side="left", padx=10)
        
        delete_button = ctk.CTkButton(
            task_frame,
            text="🗑️",
            width=40,
            command=lambda: self.delete_task(task_frame, task_id)
        )
        delete_button.pack(side="right", padx=10)
        
        self.tasks.append((task_frame, task_id))
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TodoApp()
    app.run()

