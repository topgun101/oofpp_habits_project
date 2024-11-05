import pytest
import sqlite3
import os
from example_data import add_example_habits
from habit import Habit
from completion import Completion
from analytics import get_longest_streak, get_all_habits, get_habits_by_periodicity, check_all_broken_habits

# Path to the test database for testing
TEST_DB_PATH = 'test.db'

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Initializes the SQLite database for storing habits and adds example data if it's the first time running."""
    db_exists = os.path.exists(TEST_DB_PATH)  # checks if database already exists or not

    with sqlite3.connect(TEST_DB_PATH) as db:
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

    if not db_exists:
        add_example_habits(db)
        # Teardown: Remove test.db after all tests


@pytest.fixture(scope="function", autouse=True)
def reset_database():
    """
    Reset the database state before each test.
    This ensures each test starts with the same data from example_data.py.
    """
    with sqlite3.connect(TEST_DB_PATH) as db:
        # Clear tables and re-populate with initial example data
        db.execute("DELETE FROM habits")
        db.execute("DELETE FROM completions")
        db.commit()
        add_example_habits(db)

@pytest.fixture
def habit_tracker():
    """Fixture to provide a Habit instance connected to the test database."""
    return Habit(TEST_DB_PATH)

@pytest.fixture
def completion_tracker():
    """Fixture to provide a Completion instance connected to the test database."""
    return Completion(TEST_DB_PATH)

# Utility function to create tables
def create_tables(db):
    """Create tables in the database if they don't already exist."""
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            periodicity TEXT NOT NULL,
            created_at TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY,
            habit_id INTEGER,
            completed_at TEXT,
            FOREIGN KEY(habit_id) REFERENCES habits(id)
        )
    ''')
    db.commit()

# Tests

def test_add_habit(habit_tracker):
    """Test adding a new habit."""
    habit_tracker.add_habit("Test Habit", "A test habit", "daily")
    with sqlite3.connect(TEST_DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM habits WHERE name = ?", ("Test Habit",))
        habit = cursor.fetchone()
    assert habit is not None, "Habit 'Test Habit' should have been added"

def test_prevent_duplicate_habit(habit_tracker, capsys):
    """
    Test preventing duplicate habit entries.
    Verifies that adding a habit with the same name does not insert a duplicate.
    """
    # Add the habit once
    habit_tracker.add_habit("Read Book", "Read at least one chapter", "daily")

    # Attempt to add the same habit again, expecting a duplicate prevention message
    habit_tracker.add_habit("Read Book", "Read at least one chapter again", "daily")

    # Capture the printed output (capsys Fixture: capsys is a pytest fixture that captures stdout and stderr during the test. This allows us to check for specific output messages.)
    captured = capsys.readouterr()

    # Verify that the duplicate prevention message was printed
    assert "Habit 'Read Book' already exists." in captured.out

def test_delete_habit(habit_tracker):
    """Test deleting a habit."""
    habit_tracker.add_habit("Test Habit", "A test habit", "daily")
    habit_tracker.delete_habit("Test Habit")  # Delete the added habit

    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM habits WHERE name = ?", ("Test Habit",))
        habit = cursor.fetchone()
    assert habit is None, "Habit 'Test Habit' should have been deleted."

def test_add_completion(completion_tracker):
    """Test adding a completion to a habit."""
    completion_tracker.add_completion("Read Book")
    with sqlite3.connect(TEST_DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM completions WHERE habit_id = (SELECT id FROM habits WHERE name = 'Read Book')")
        completion = cursor.fetchone()
    assert completion is not None, "Completion should have been recorded for 'Read Book'"

def test_check_habits(capsys):
    """Test checking for broken habits."""
    # Assuming 'check_all_broken_habits' returns a list of broken habits
    broken_habits = check_all_broken_habits()

    # Capture output and verify that broken habits are listed
    captured = capsys.readouterr()
    for habit_name, days in broken_habits:
        assert f"Habit '{habit_name}' is broken" in captured.out

def test_list_habits(capsys):
    """Test listing all habits."""
    # Call list_habits (assuming it prints habit names)
    get_all_habits()

    # Capture printed output
    captured = capsys.readouterr()

    # Check if each example habit is listed
    expected_habits = ["Exercise", "Read Book", "Meditate", "Write Journal", "Grocery Shopping"]
    for habit in expected_habits:
        assert habit in captured.out, f"Habit '{habit}' should be listed in output."

def test_list_by_period(capsys):
    """Test listing habits by periodicity."""
    # List daily habits
    get_habits_by_periodicity("daily")
    captured_daily = capsys.readouterr()

    # Verify that only daily habits are listed
    daily_habits = ["Exercise", "Read Book", "Write Journal"]
    for habit in daily_habits:
        assert habit in captured_daily.out, f"Daily habit '{habit}' should be listed."

def test_longest_streak_for_specific_habit(habit_tracker, completion_tracker):
    """Test calculating the longest streak for a specific habit."""
    habit, streak, period_type = get_longest_streak("Read Book")
    assert habit == "Read Book", "The habit name should be 'Read Book'"
    assert streak >= 1, "The streak for 'Read Book' should be at least 1 day"
    assert period_type == "days", "The period type should be 'days' for a daily habit"

def test_longest_streak_across_all_habits(habit_tracker, completion_tracker):
    """Test calculating the longest streak across all habits."""
    habit, streak, period_type = get_longest_streak()
    assert habit in ["Read Book", "Exercise"], "The habit with the longest streak should be one of the tracked habits"
    assert streak >= 1, "The longest streak should be at least 1"
    assert period_type in ["days", "weeks"], "The period type should be either 'days' or 'weeks'"