import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime
import json
import os


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced To-Do List with Time Selection")
        self.root.geometry("600x700")
        
        # Set the default colors
        self.root.configure(bg='black')
        
        self.main_color = 'black'  # Black for the background
        self.accent_color = '#800080'  # Purple for accents
        self.input_color = '#800080'  # Purple for input fields
        
        # Task storage
        self.tasks = []
        self.task_file = "tasks.json"
        self.log_file = "task_log.txt"
        self.load_tasks()

        # Title Label
        title_label = tk.Label(root, text="To-Do List", font=("Arial", 16, "bold"), fg=self.accent_color, bg=self.main_color)
        title_label.pack(pady=10, anchor="w", padx=20)

        # Task Entry Frame
        entry_frame = tk.Frame(root, bg=self.main_color)
        entry_frame.pack(pady=10, anchor="w", padx=20)
        self.task_name_var = tk.StringVar()
        self.task_duration_var = tk.StringVar()
        self.priority_var = tk.StringVar(value="Medium Priority")  # Default priority
        self.start_hour_var = tk.StringVar()
        self.start_min_var = tk.StringVar()
        self.end_hour_var = tk.StringVar()
        self.end_min_var = tk.StringVar()
        self.task_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))  # Fixed here
        self.start_am_pm_var = tk.StringVar(value="AM")
        self.end_am_pm_var = tk.StringVar(value="AM")

        # Task Name Entry
        tk.Label(entry_frame, text="Task:", font=("Arial", 12), fg='white', bg=self.main_color).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.task_name_entry = tk.Entry(entry_frame, textvariable=self.task_name_var, width=30, bg=self.input_color, fg='white')
        self.task_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Task Duration Entry
        tk.Label(entry_frame, text="Duration:", font=("Arial", 12), fg='white', bg=self.main_color).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.task_duration_entry = tk.Entry(entry_frame, textvariable=self.task_duration_var, width=30, bg=self.input_color, fg='white')
        self.task_duration_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Priority Option Menu
        tk.Label(entry_frame, text="Priority:", font=("Arial", 12), fg='white', bg=self.main_color).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        priority_options = ["High Priority", "Medium Priority", "Low Priority"]
        self.priority_menu = tk.OptionMenu(entry_frame, self.priority_var, *priority_options)
        self.priority_menu.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Time Input Fields (Manual Entry for Hours/Minutes, AM/PM selection)
        tk.Label(entry_frame, text="Start Time (AM/PM):", font=("Arial", 12), fg='white', bg=self.main_color).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        
        # Start Time (Hour and Minute Entry)
        self.start_hour_entry = tk.Entry(entry_frame, textvariable=self.start_hour_var, width=5, bg=self.input_color, fg='white')
        self.start_hour_entry.grid(row=3, column=1, padx=5, sticky="w")
        self.start_min_entry = tk.Entry(entry_frame, textvariable=self.start_min_var, width=5, bg=self.input_color, fg='white')
        self.start_min_entry.grid(row=3, column=1, padx=50, sticky="w")
        
        self.start_am_pm_menu = tk.OptionMenu(entry_frame, self.start_am_pm_var, "AM", "PM")
        self.start_am_pm_menu.grid(row=3, column=2, padx=5, sticky="w")

        tk.Label(entry_frame, text="End Time (AM/PM):", font=("Arial", 12), fg='white', bg=self.main_color).grid(row=4, column=0, padx=5, pady=5, sticky="w")
        
        # End Time (Hour and Minute Entry)
        self.end_hour_entry = tk.Entry(entry_frame, textvariable=self.end_hour_var, width=5, bg=self.input_color, fg='white')
        self.end_hour_entry.grid(row=4, column=1, padx=5, sticky="w")
        self.end_min_entry = tk.Entry(entry_frame, textvariable=self.end_min_var, width=5, bg=self.input_color, fg='white')
        self.end_min_entry.grid(row=4, column=1, padx=50, sticky="w")
        
        self.end_am_pm_menu = tk.OptionMenu(entry_frame, self.end_am_pm_var, "AM", "PM")
        self.end_am_pm_menu.grid(row=4, column=2, padx=5, sticky="w")

        # Calendar Toggle Button
        self.calendar_button = tk.Button(entry_frame, text="Show Calendar", command=self.toggle_calendar, fg='white', bg=self.accent_color)
        self.calendar_button.grid(row=5, column=0, columnspan=2, pady=10, sticky="w")
        self.calendar_visible = False
        self.calendar = Calendar(entry_frame, selectmode='day', date_pattern='yyyy-mm-dd', textvariable=self.task_date_var)
        self.calendar.grid(row=6, column=0, columnspan=2, pady=5)
        self.calendar.grid_remove()

        # Add Task Button
        self.add_button = tk.Button(entry_frame, text="Add Task", command=self.add_task, fg='white', bg=self.accent_color)
        self.add_button.grid(row=7, column=0, columnspan=2, pady=10, sticky="w")

        # Bind Enter key to the add_task function
        root.bind('<Return>', lambda event: self.add_task())

        # Task List Frame
        self.task_list_frame = tk.Frame(root, bg=self.main_color)
        self.task_list_frame.pack(pady=10, fill="both", expand=True, anchor="w", padx=20)

        # Task List Display (with checkboxes)
        self.update_task_list()

    def toggle_calendar(self):
        if self.calendar_visible:
            self.calendar.grid_remove()
            self.calendar_button.config(text="Show Calendar")
        else:
            self.calendar.grid()
            self.calendar_button.config(text="Hide Calendar")
        self.calendar_visible = not self.calendar_visible

    def add_task(self):
        task_name = self.task_name_var.get().strip()
        task_duration = self.task_duration_var.get().strip()
        priority = self.priority_var.get()
        selected_date = self.task_date_var.get()
        start_time = f"{self.start_hour_var.get()}:{self.start_min_var.get()} {self.start_am_pm_var.get()}"
        end_time = f"{self.end_hour_var.get()}:{self.end_min_var.get()} {self.end_am_pm_var.get()}"

        # Validate input
        if not task_name:
            messagebox.showerror("Input Error", "Task name is required.")
            return

        # Time validation
        if "HH" in start_time or "MM" in start_time or "HH" in end_time or "MM" in end_time:
            time_range = "No Time"
        else:
            try:
                start_dt = datetime.strptime(start_time, "%I:%M %p")
                end_dt = datetime.strptime(end_time, "%I:%M %p")
                if start_dt >= end_dt:
                    messagebox.showerror("Input Error", "Start time must be earlier than end time.")
                    return
                time_range = f"{start_time} to {end_time}"
            except ValueError:
                messagebox.showerror("Input Error", "Invalid time format.")
                return

        task = {
            "name": task_name,
            "duration": task_duration if task_duration else "No Duration",
            "priority": priority,
            "date": selected_date,
            "time": time_range,
            "completed": False  # Add a 'completed' field to track if a task is checked
        }

        self.tasks.append(task)
        self.log_action("Added", task)
        self.save_tasks()
        self.update_task_list()

        # Reset input fields
        self.task_name_var.set("")
        self.task_duration_var.set("")
        self.start_hour_var.set("")
        self.start_min_var.set("")
        self.end_hour_var.set("")
        self.end_min_var.set("")
        self.task_date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.start_am_pm_var.set("AM")
        self.end_am_pm_var.set("AM")

    def update_task_list(self):
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()

        for idx, task in enumerate(self.tasks):
            task_frame = tk.Frame(self.task_list_frame, bg=self.main_color)
            task_frame.pack(fill="x", pady=5, anchor="w")

            # Set color based on priority
            if task['priority'] == "High Priority":
                priority_color = "red"
            elif task['priority'] == "Low Priority":
                priority_color = "green"
            else:
                priority_color = "yellow"

            task_label = tk.Label(task_frame, text=f"{task['name']} - {task['date']} - {task['time']} - {task['priority']}", 
                                  fg='white', bg=self.main_color, width=60, anchor="w")
            task_label.pack(side="left", padx=10)
            
            checkbox_var = tk.BooleanVar()
            checkbox = tk.Checkbutton(task_frame, variable=checkbox_var, bg=self.main_color, 
                                      command=lambda idx=idx, var=checkbox_var: self.toggle_task_check(idx, var))
            checkbox.pack(side="left", padx=10)

    def toggle_task_check(self, idx, var):
        task = self.tasks[idx]
        task["completed"] = var.get()
        if task["completed"]:
            self.tasks.pop(idx)  # Delete the task when checked off
            self.update_task_list()
            self.save_tasks()
            self.log_action("Completed and Deleted", task)
        else:
            self.save_tasks()

    def log_action(self, action, task):
        log_entry = f"{action}: {task['name']} - {task['date']} ({task['priority']}) - {task['time']}\n"
        with open(self.log_file, "a") as log:
            log.write(log_entry)

    def save_tasks(self):
        with open(self.task_file, "w") as file:
            json.dump(self.tasks, file)

    def load_tasks(self):
        if os.path.exists(self.task_file):
            with open(self.task_file, "r") as file:
                self.tasks = json.load(file)


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
