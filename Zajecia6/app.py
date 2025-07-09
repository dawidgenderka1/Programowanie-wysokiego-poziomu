from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET', 'POST'])
def tasks_page():
    if request.method == 'POST':
        task_content = request.form.get('task')
        if task_content:
            tasks.append({'id': len(tasks), 'content': task_content, 'done': False})
        return redirect(url_for('tasks_page'))
    return render_template('tasks.html', tasks=tasks)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/delete/<int:id>')
def delete_task(id):
    global tasks
    tasks = [task for task in tasks if task['id'] != id]
    return redirect(url_for('tasks_page'))

@app.route('/done/<int:id>')
def mark_done(id):
    for task in tasks:
        if task['id'] == id:
            task['done'] = not task['done']
    return redirect(url_for('tasks_page'))

if __name__ == '__main__':
    app.run(debug=True)