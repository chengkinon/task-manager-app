from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = "tasks.db"

# Initialize Database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        description TEXT NOT NULL,
                        deadline TEXT,
                        completed INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

# Home Page: Display Tasks
@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Add Task
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        description = request.form['description']
        deadline = request.form['deadline']
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (description, deadline) VALUES (?, ?)", (description, deadline))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_task.html')

# Update Task
@app.route('/update/<int:task_id>')
def update_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Delete Task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
