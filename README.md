# ScholarMate

A Flask-based web application for managing scholarship data. Keep track of scholarship opportunities, deadlines, and bookmark your favorites.

## Features

- Add new scholarship entries with detailed information
- View all scholarships in a clean, organized table
- Bookmark important scholarships
- View only bookmarked scholarships
- Get alerts for scholarships with deadlines within 30 days
- Responsive design that works on all devices

## Deployment Instructions

### PythonAnywhere Deployment

1. Sign up for a free account at [PythonAnywhere](https://www.pythonanywhere.com/)

2. Once logged in, go to the Dashboard and click on "Web" tab

3. Click on "Add a new web app"

4. Choose "Manual configuration" and select Python 3.8

5. In the "Code" section:
   - Set the working directory to your project directory
   - Set the WSGI configuration file to `/var/www/yourusername_pythonanywhere_com_wsgi.py`

6. In the "Virtualenv" section:
   - Create a new virtualenv
   - Install requirements using: `pip install -r requirements.txt`

7. In the "Files" section:
   - Upload your project files
   - Make sure to upload the database file (scholarships.db)

8. In the "Web" section:
   - Set the WSGI configuration file to point to your wsgi.py
   - Add the following to the WSGI file:
     ```python
     import sys
     import os
     path = '/home/yourusername/yourproject'
     if path not in sys.path:
         sys.path.append(path)
     from app import app as application
     ```

9. Click "Reload" to start your application

### Important Notes

1. Make sure to set a proper SECRET_KEY in your app.py:
   ```python
   app.secret_key = 'your-secret-key-here'  # Replace with a secure key
   ```

2. The database file (scholarships.db) needs to be uploaded to PythonAnywhere

3. Make sure all file permissions are set correctly

4. If you need to make changes to the database, you can use the PythonAnywhere console

## Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   python init_db.py
   ```

4. Run the application:
   ```bash
   python app.py
   ```

The application will be available at http://localhost:5001

## Database

The application uses SQLite as its database. The database file (`scholarships.db`) will be automatically created when you first run the application.

## Project Structure

```
ScholarMate/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── static/
│   └── style.css      # CSS styles
└── templates/         # HTML templates
    ├── base.html      # Base template
    ├── index.html     # Homepage
    ├── add.html       # Add scholarship form
    ├── view.html      # View all scholarships
    ├── bookmarks.html # View bookmarked scholarships
    └── alerts.html    # View upcoming deadlines
```

## Contributing

Feel free to submit issues and enhancement requests! 