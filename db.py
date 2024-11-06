import sqlite3
from example_data import add_example_habits  # function for adding example data
import os # used for checking if database file already exists

# Default path for the database
# Use 'data.db' as default or test.db for testing with pytest
DB_PATH = 'data.db'

### database initialization incl. example data

def init_db():
    """
    the init_db is called in the main.py and test_habit_tracker.py
    in order to generate the main data.db or for testing purposes the test.db

    It initializes the SQLite database for storing habits and
    adds example data if it's the first time generating the DB.
    """
    db_exists = os.path.exists(DB_PATH) # checks if database already exists or not
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                periodicity TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS completions (
                habit_id INTEGER,
                completed_at TEXT NOT NULL,
                FOREIGN KEY(habit_id) REFERENCES habits(id)
            )
        ''')
    db.commit()

### adds example data to the database if the DB is generated for the first time
    if not db_exists:
        add_example_habits(db)