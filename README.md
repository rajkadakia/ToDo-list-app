# ToDo-list-app
# 📝 Enhanced To-Do List with Time Selection

This is a simple yet feature-rich To-Do List desktop application built with Python's Tkinter library. It allows users to manage tasks with additional time, date, and priority features — all styled in a sleek dark mode interface.

---

## ✅ Features

- 🖤 **Dark-themed UI** with purple accents
- 📅 **Date selection** using an integrated calendar (`tkcalendar`)
- ⏰ **Manual time input** (start and end) with AM/PM support
- ⌛ **Optional task duration field**
- ⚡ **Priority levels**: High, Medium, Low
- ✔️ **Mark tasks complete** with a checkbox (task auto-removal)
- 💾 **Persistent storage** in `tasks.json`
- 🧾 **Action logging** to `task_log.txt`

---

## 🔧 Requirements

- Python 3.x
- `tkinter` (comes bundled with Python)
- `tkcalendar`

Install `tkcalendar` using pip:

``bash
pip install tkcalendar
How to Run
Save the code in a Python file, e.g., todo_app.py

Run the file:

bash
Copy
Edit
python todo_app.py
Start adding tasks with details like name, date, time, and priority!

 Usage Notes
Use the Show Calendar button to pick a task date.

Enter start and end times in 12-hour format and select AM/PM.

You can skip time entry; the task will show "No Time".

Checking a task immediately removes it and logs the action.

All tasks are saved in tasks.json.

Actions like addition or completion are logged in task_log.txt.
This project is open source
