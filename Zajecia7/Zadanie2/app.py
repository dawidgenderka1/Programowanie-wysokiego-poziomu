from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the database and add sample teachers
def init_db():
    conn = sqlite3.connect('teachers.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            subject TEXT NOT NULL,
            time TEXT NOT NULL
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM teachers")
    if cursor.fetchone()[0] == 0:
        sample_teachers = [
            ('Dariusz Petyla', 'Matematyka', 'Mon 10:00-12:00'),
            ('Dominika Puchodolska', 'Fizyka', 'Tue 14:00-16:00'),
            ('Krystian Owczarek', 'Angielski', 'Wed 09:00-11:00')
        ]
        cursor.executemany('INSERT INTO teachers (name, subject, time) VALUES (?, ?, ?)', sample_teachers)
    conn.commit()
    conn.close()

def display_teachers():
    conn = sqlite3.connect('teachers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, subject FROM teachers')
    teachers = cursor.fetchall()
    conn.close()
    return teachers

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/teachers', methods=['GET', 'POST'])
def teachers_page():
    if request.method == 'POST':
        name = request.form.get('name')
        subject = request.form.get('subject')
        time = request.form.get('time')
        if name and subject and time:
            conn = sqlite3.connect('teachers.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO teachers (name, subject, time) VALUES (?, ?, ?)', (name, subject, time))
            conn.commit()
            conn.close()
        return redirect(url_for('teachers_page'))
    
    teachers = display_teachers()
    return render_template('teachers.html', teachers=teachers)

@app.route('/delete/<int:id>')
def delete_teacher(id):
    conn = sqlite3.connect('teachers.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM teachers WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('teachers_page'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)