# personal_task_manager

This is a simple Task Manager application built using Python and Tkinter for the graphical user interface (GUI). It allows users to manage tasks by adding, deleting, and sorting them based on priority or deadline. The application uses SQLite as the database to store tasks.

There are also added files with html and css for front end use.

Features

Add tasks: Users can enter task details, including title, description, priority, and deadline

Delete tasks: Users can remove tasks from the list

Sort tasks: Tasks can be sorted by priority or deadline

Persistent storage: Tasks are stored in an SQLite database

Priority based coloring:

High priority: Red

Medium priority: Yellow

Low priority: Green

Date validation: Prevents setting deadlines in the past.

Requirements

To run this application, you need the following Python packages:

tkinter (included with Python)

sqlite3 (included with Python)

tkcalendar (for the date picker)

You can install the tkcalendar package using pip

Code Structure

Database functions:

init_db(): Initializes the SQLite database and creates the tasks table

add_task(): Adds a new task to the database

fetch_tasks(): Fetches tasks from the database, optionally sorted by priority or deadline

delete_task(): Deletes a task from the database

reset_autoincrement(): Resets the auto-increment counter for task IDs when all tasks are deleted

GUI:

The TaskManagerApp class handles the GUI and user interactions

The main window displays a list of tasks in a Treeview widget

Users can add tasks using a pop-up window with input fields for task details



