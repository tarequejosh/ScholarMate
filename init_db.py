import sqlite3
import os

def init_database():
    # Remove existing database if it exists
    if os.path.exists('scholarships.db'):
        os.remove('scholarships.db')
    
    # Create new database
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
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_database() 