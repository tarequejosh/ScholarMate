from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('scholarships.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scholarships
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  country TEXT NOT NULL,
                  university TEXT NOT NULL,
                  degree_level TEXT NOT NULL,
                  field_of_study TEXT NOT NULL,
                  deadline DATE NOT NULL,
                  link TEXT NOT NULL,
                  is_bookmarked BOOLEAN DEFAULT 0)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_scholarship():
    if request.method == 'POST':
        conn = sqlite3.connect('scholarships.db')
        c = conn.cursor()
        c.execute('''INSERT INTO scholarships 
                    (name, country, university, degree_level, field_of_study, deadline, link)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                 (request.form['name'],
                  request.form['country'],
                  request.form['university'],
                  request.form['degree_level'],
                  request.form['field_of_study'],
                  request.form['deadline'],
                  request.form['link']))
        conn.commit()
        conn.close()
        return redirect(url_for('view_scholarships'))
    return render_template('add.html')

@app.route('/view')
def view_scholarships():
    conn = sqlite3.connect('scholarships.db')
    c = conn.cursor()
    c.execute('SELECT * FROM scholarships ORDER BY deadline')
    scholarships = c.fetchall()
    conn.close()
    return render_template('view.html', scholarships=scholarships)

@app.route('/bookmarks')
def view_bookmarks():
    conn = sqlite3.connect('scholarships.db')
    c = conn.cursor()
    c.execute('SELECT * FROM scholarships WHERE is_bookmarked = 1 ORDER BY deadline')
    scholarships = c.fetchall()
    conn.close()
    return render_template('bookmarks.html', scholarships=scholarships)

@app.route('/alerts')
def view_alerts():
    conn = sqlite3.connect('scholarships.db')
    c = conn.cursor()
    thirty_days_later = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    c.execute('SELECT * FROM scholarships WHERE deadline <= ? ORDER BY deadline', (thirty_days_later,))
    scholarships = c.fetchall()
    conn.close()
    return render_template('alerts.html', scholarships=scholarships)

@app.route('/toggle_bookmark/<int:scholarship_id>')
def toggle_bookmark(scholarship_id):
    conn = sqlite3.connect('scholarships.db')
    c = conn.cursor()
    c.execute('UPDATE scholarships SET is_bookmarked = NOT is_bookmarked WHERE id = ?', (scholarship_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_scholarships'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True) 