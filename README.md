# ScholarMate

A Flask-based web application for managing scholarship data. Keep track of scholarship opportunities, deadlines, and bookmark your favorites.

## Features

- Add new scholarship entries with detailed information
- View all scholarships in a clean, organized table
- Bookmark important scholarships
- View only bookmarked scholarships
- Get alerts for scholarships with deadlines within 30 days
- Responsive design that works on all devices

## Setup

1. Clone the repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Make sure you're in the project directory
2. Run the Flask application:
   ```bash
   python app.py
   ```
3. Open your web browser and navigate to `http://localhost:5000`

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