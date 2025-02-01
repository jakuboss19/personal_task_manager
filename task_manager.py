import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkcalendar import DateEntry
from datetime import datetime

# Initialize database connection
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT,
                        priority TEXT,
                        deadline TEXT)''')
    conn.commit()
    conn.close()

# Add a task to the database
def add_task(title, description, priority, deadline):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description, priority, deadline) VALUES (?, ?, ?, ?)",
                   (title, description, priority, deadline))
    conn.commit()
    conn.close()

# Fetch all tasks from the database
def fetch_tasks(order_by="deadline"):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    if order_by == "priority":
        cursor.execute("""
            SELECT * FROM tasks
            ORDER BY
                CASE priority           # order by priority, not by alphabet
                    WHEN 'High' THEN 1     
                    WHEN 'Medium' THEN 2
                    WHEN 'Low' THEN 3
                END
        """)
    
else:
    cursor.execute(f"SELECT * FROM tasks ORDER BY {order_by}")
    
    
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# Delete task from database
def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def reset_autoincrement():
    """Reset ID's when all tasks are deleted"""
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='tasks'")  
    conn.commit()
    conn.close()
    


# Main Application Class
class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")

        # Frame for Task List
        self.task_frame = ttk.Frame(self.root)
        self.task_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Option for sorting
        self.sort_var = tk.StringVar(value="deadline")
        sort_frame = ttk.Frame(self.root)
        sort_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(sort_frame, text="Sort by:").pack(side=tk.LEFT)
        sort_menu = ttk.Combobox(sort_frame, textvariable=self.sort_var, values=["priority", "deadline"], state="readonly")
        sort_menu.pack(side=tk.LEFT, padx=5)
        sort_menu.bind("<<ComboboxSelected>>", lambda e: self.load_tasks())

        # Treeview for tasks
        self.tree = ttk.Treeview(self.task_frame, columns=("ID", "Title", "Description", "Priority", "Deadline"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Deadline", text="Deadline")
        self.tree.column("ID", width=50)
        self.tree.column("Title", width=200)
        self.tree.column("Description", width=300)
        self.tree.column("Priority", width=100)
        self.tree.column("Deadline", width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Frame for Buttons
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(fill=tk.X, padx=10, pady=5)

        self.add_button = ttk.Button(self.button_frame, text="Add Task", command=self.open_add_task_window)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ttk.Button(self.button_frame, text="Delete Task", command=self.delete_selected_task)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # self.refresh_button = ttk.Button(self.button_frame, text="Refresh", command=self.load_tasks)
        # self.refresh_button.pack(side=tk.LEFT, padx=5)

        # Load tasks into the Treeview
        self.load_tasks()

    def open_add_task_window(self):
        def on_save_task():
            title = title_entry.get()
            description = description_text.get("1.0", tk.END).strip()
            priority = priority_combobox.get()
            deadline = deadline_entry.get()

            if not title or not priority or not deadline:
                messagebox.showerror("Error", "Title, Priority, and Deadline are required!")
                return

            add_task(title, description, priority, deadline)
            messagebox.showinfo("Success", "Task added successfully!")
            add_task_window.destroy()
            self.load_tasks()

        def validate_date(event):
            """Validate date in calendar so its not possible to set deadline in past"""
            selected_date = deadline_entry.get_date()
            today = datetime.today().date()

            if selected_date < today:
                messagebox.showerror("Invalid date", "The deadline can't be in the past!")
                deadline_entry.set_date(today)


        add_task_window = tk.Toplevel(self.root)
        add_task_window.title("Add Task")

        ttk.Label(add_task_window, text="Title:").pack(padx=10, pady=5, anchor=tk.W)
        title_entry = ttk.Entry(add_task_window)
        title_entry.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(add_task_window, text="Description:").pack(padx=10, pady=5, anchor=tk.W)
        description_text = tk.Text(add_task_window, height=5)
        description_text.pack(fill=tk.BOTH, padx=10, pady=5)

        ttk.Label(add_task_window, text="Priority:").pack(padx=10, pady=5, anchor=tk.W)
        priority_combobox = ttk.Combobox(add_task_window, values=["High", "Medium", "Low"], state="readonly")
        priority_combobox.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(add_task_window, text="Deadline (YYYY-MM-DD):").pack(padx=10, pady=5, anchor=tk.W)
        deadline_entry = DateEntry(add_task_window, date_pattern="yyyy-mm-dd")
        deadline_entry.pack(fill=tk.X, padx=10, pady=5)
        deadline_entry.set_date(datetime.today().date()) 
        deadline_entry.bind("<<DateEntrySelected>>", validate_date) 

        save_button = ttk.Button(add_task_window, text="Save", command=on_save_task)
        save_button.pack(pady=10)

    def delete_selected_task(self):
        """Delete selected task"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error","Please select a task to delete!")
            return

        task_id = self.tree.item(selected_item[0], "values")[0]
        delete_task(task_id)
        
        if not fetch_tasks():
            reset_autoincrement()
        
        messagebox.showinfo("Success", "Task deleted successfully!")
        self.load_tasks()

    def load_tasks(self):
        """Clear current tasks"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Fetch tasks from the database and load into the Treeview
        for task in fetch_tasks(self.sort_var.get()):
            row_id = self.tree.insert("", tk.END, values=(task[0], task[1], task[2], task[3], task[4]))
            if task[3] == "High":
                self.tree.item(row_id, tags=("high",))
            elif task[3] == "Medium":
                self.tree.item(row_id, tags=("medium",))
            else:
                self.tree.item(row_id, tags=("low",))
        self.tree.tag_configure("high", background="red")
        self.tree.tag_configure("medium", background="yellow")
        self.tree.tag_configure("low", background="green")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
