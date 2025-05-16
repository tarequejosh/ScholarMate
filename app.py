from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'scholarmate-secret-key-2024'  # Replace this with a secure key in production

def init_db():
    conn = sqlite3.connect('scholarships.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Create scholarships table
    c.execute('''CREATE TABLE IF NOT EXISTS scholarships
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  country TEXT NOT NULL,
                  university TEXT NOT NULL,
                  degree_level TEXT NOT NULL,
                  field_of_study TEXT NOT NULL,
                  deadline DATE NOT NULL,
                  link TEXT NOT NULL,
                  is_bookmarked BOOLEAN DEFAULT 0,
                  user_id INTEGER,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    conn.commit()
    conn.close()

# Login required decorator
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        conn = sqlite3.connect('scholarships.db')
        c = conn.cursor()
        
        try:
            hashed_password = generate_password_hash(password)
            c.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                     (username, hashed_password, email))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists.', 'error')
        finally:
            conn.close()
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('scholarships.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Logged in successfully!', 'success')
            return redirect(url_for('view_scholarships'))
        else:
            flash('Invalid username or password.', 'error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_scholarship():
    if request.method == 'POST':
        conn = sqlite3.connect('scholarships.db')
        c = conn.cursor()
        c.execute('''INSERT INTO scholarships 
                    (name, country, university, degree_level, field_of_study, deadline, link, user_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                 (request.form['name'],
                  request.form['country'],
                  request.form['university'],
                  request.form['degree_level'],
                  request.form['field_of_study'],
                  request.form['deadline'],
                  request.form['link'],
                  session['user_id']))
        conn.commit()
        conn.close()
        flash('Scholarship added successfully!', 'success')
        return redirect(url_for('view_scholarships'))
    return render_template('add.html')

@app.route('/view')
@login_required
def view_scholarships():
    conn = sqlite3.connect('scholarships.db')
    c = conn.cursor()
    c.execute('SELECT * FROM scholarships WHERE user_id = ? ORDER BY deadline', (session['user_id'],))
    scholarships = c.fetchall()
    conn.close()
    return render_template('view.html', scholarships=scholarships)

@app.route('/bookmarks')
@login_required
def view_bookmarks():
    conn = sqlite3.connect('scholarships.db')
    c = conn.cursor()
    c.execute('SELECT * FROM scholarships WHERE is_bookmarked = 1 AND user_id = ? ORDER BY deadline', (session['user_id'],))
    scholarships = c.fetchall()
    conn.close()
    return render_template('bookmarks.html', scholarships=scholarships)

@app.route('/alerts')
@login_required
def view_alerts():
    conn = sqlite3.connect('scholarships.db')
    c = conn.cursor()
    thirty_days_later = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    c.execute('SELECT * FROM scholarships WHERE deadline <= ? AND user_id = ? ORDER BY deadline', 
             (thirty_days_later, session['user_id']))
    scholarships = c.fetchall()
    conn.close()
    return render_template('alerts.html', scholarships=scholarships)

@app.route('/toggle_bookmark/<int:scholarship_id>')
@login_required
def toggle_bookmark(scholarship_id):
    conn = sqlite3.connect('scholarships.db')
    c = conn.cursor()
    c.execute('UPDATE scholarships SET is_bookmarked = NOT is_bookmarked WHERE id = ? AND user_id = ?', 
             (scholarship_id, session['user_id']))
    conn.commit()
    conn.close()
    return redirect(url_for('view_scholarships'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001) 