from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET', 'POST'])
def tasks_page():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        task_content = request.form.get('task')
        if task_content:
            cursor.execute('INSERT INTO tasks (content, done) VALUES (?, ?)', (task_content, False))
            conn.commit()
        conn.close()
        return redirect(url_for('tasks_page'))
    
    cursor.execute('SELECT id, content, done FROM tasks')
    tasks = [{'id': row[0], 'content': row[1], 'done': row[2]} for row in cursor.fetchall()]
    conn.close()
    return render_template('tasks.html', tasks=tasks)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/delete/<int:id>')
def delete_task(id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('tasks_page'))

@app.route('/done/<int:id>')
def mark_done(id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET done = NOT done WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('tasks_page'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)