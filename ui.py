import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, timedelta
import requests
import threading

API_URL = "http://localhost:5000"

class TaskManagementUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Management System")
        self.root.geometry("800x600")
        
        # Create main frames
        self.create_widgets()
        self.refresh_tasks()
        
    def create_widgets(self):
        # Top frame for controls
        top_frame = ttk.Frame(self.root)
        top_frame.pack(pady=10, padx=10, fill=tk.X)
        
        ttk.Label(top_frame, text="Title:").pack(side=tk.LEFT, padx=5)
        self.title_entry = ttk.Entry(top_frame, width=30)
        self.title_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(top_frame, text="Due Date (YYYY-MM-DD):").pack(side=tk.LEFT, padx=5)
        self.date_entry = ttk.Entry(top_frame, width=15)
        self.date_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(top_frame, text="Create Task", command=self.create_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Refresh", command=self.refresh_tasks).pack(side=tk.LEFT, padx=5)
        
        # Treeview for displaying tasks
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Title", "Due Date", "Completed"), height=15, yscrollcommand=scrollbar.set)
        self.tree.heading('#0', text='')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Due Date', text='Due Date')
        self.tree.heading('Completed', text='Completed')
        
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', anchor=tk.CENTER, width=40)
        self.tree.column('Title', anchor=tk.W, width=300)
        self.tree.column('Due Date', anchor=tk.CENTER, width=120)
        self.tree.column('Completed', anchor=tk.CENTER, width=80)
        
        scrollbar.config(command=self.tree.yview)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bottom frame for action buttons
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(pady=10, padx=10, fill=tk.X)
        
        ttk.Button(bottom_frame, text="Toggle Completion", command=self.toggle_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="Delete Selected", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        
        self.status_label = ttk.Label(bottom_frame, text="Ready")
        self.status_label.pack(side=tk.RIGHT, padx=5)
    
    def get_selected_task_id(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task first")
            return None
        item = self.tree.item(selected[0])
        return int(item['values'][0])
    
    def create_task(self):
        title = self.title_entry.get().strip()
        due_date = self.date_entry.get().strip()
        
        if not title or not due_date:
            messagebox.showerror("Error", "Please enter both title and due date")
            return
        
        def thread_create():
            try:
                response = requests.post(f"{API_URL}/tasks", json={"title": title, "due_date": due_date})
                if response.status_code == 201:
                    self.title_entry.delete(0, tk.END)
                    self.date_entry.delete(0, tk.END)
                    self.refresh_tasks()
                    self.status_label.config(text="Task created successfully")
                else:
                    messagebox.showerror("Error", f"Failed to create task: {response.json()['error']}")
            except Exception as e:
                messagebox.showerror("Error", f"Connection error: {str(e)}")
        
        thread = threading.Thread(target=thread_create, daemon=True)
        thread.start()
    
    def refresh_tasks(self):
        def thread_refresh():
            try:
                response = requests.get(f"{API_URL}/tasks")
                if response.status_code == 200:
                    tasks = response.json()
                    self.root.after(0, lambda: self.update_tree(tasks))
                    self.status_label.config(text=f"Loaded {len(tasks)} tasks")
            except Exception as e:
                self.status_label.config(text=f"Error: {str(e)}")
        
        thread = threading.Thread(target=thread_refresh, daemon=True)
        thread.start()
    
    def update_tree(self, tasks):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for task in tasks:
            completed_status = "✓" if task['completed'] else "✗"
            self.tree.insert('', tk.END, values=(
                task['id'],
                task['title'],
                task['due_date'],
                completed_status
            ))
    
    def toggle_task(self):
        task_id = self.get_selected_task_id()
        if task_id is None:
            return
        
        def thread_toggle():
            try:
                response = requests.patch(f"{API_URL}/tasks/{task_id}/toggle")
                if response.status_code == 200:
                    self.refresh_tasks()
                    self.status_label.config(text="Task toggled successfully")
                else:
                    messagebox.showerror("Error", "Failed to toggle task")
            except Exception as e:
                messagebox.showerror("Error", f"Connection error: {str(e)}")
        
        thread = threading.Thread(target=thread_toggle, daemon=True)
        thread.start()
    
    def delete_task(self):
        task_id = self.get_selected_task_id()
        if task_id is None:
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
            def thread_delete():
                try:
                    response = requests.delete(f"{API_URL}/tasks/{task_id}")
                    if response.status_code == 200:
                        self.refresh_tasks()
                        self.status_label.config(text="Task deleted successfully")
                    else:
                        messagebox.showerror("Error", "Failed to delete task")
                except Exception as e:
                    messagebox.showerror("Error", f"Connection error: {str(e)}")
            
            thread = threading.Thread(target=thread_delete, daemon=True)
            thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagementUI(root)
    root.mainloop()
