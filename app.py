from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

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
                CASE priority
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
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='tasks'")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    tasks = fetch_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task_route():
    title = request.form['title']
    description = request.form['description']
    priority = request.form['priority']
    deadline = request.form['deadline']

    if not title or not priority or not deadline:
        return "Title, Priority, and Deadline are required!", 400

    add_task(title, description, priority, deadline)
    return redirect(url_for('index'))

@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task_route(task_id):
    delete_task(task_id)
    remaining_tasks = fetch_tasks()
    if not remaining_tasks:
        reset_autoincrement()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
