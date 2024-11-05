import os
from db import init_db, DB_PATH  # Import the DB_PATH
import pytest
import sqlite3
from example_data import add_example_habits
from habit import Habit
from completion import Completion
from analytics import get_longest_streak, get_all_habits, get_habits_by_periodicity, check_all_broken_habits

@pytest.fixture(scope="session", autouse=True) #Die Fixture ist so konfiguriert, dass sie einmal pro Testlauf automatisch vor allen Tests ausgeführt wird.
def setup_test_database():
    """
    Initializes the SQLite test database with tables if it doesn't already exist.
    Populates it with fixed test example data.
    """
    db_exists = os.path.exists(DB_PATH)
    # Lösche die bestehende test.db, falls sie existiert
    if db_exists:
        os.remove('test.db')

    # Erstelle die Datenbank neu und initialisiere sie
    with sqlite3.connect(DB_PATH) as db:
        init_db()  # Tabellen in der Datenbank initialisieren
        add_example_habits(db, test_data=True)  # Testdaten hinzufügen

#    with sqlite3.connect(DB_PATH) as db:
        # Create tables if they don't exist
#        init_db()  # Initialize tables

        # If the database is newly created, add example data
#        if not db_exists:
            # Populate with example data using test data for consistent test results
#            add_example_habits(db, test_data=True)


@pytest.fixture
def habit_tracker():
    """Fixture to provide a Habit instance connected to the test database."""
    return Habit(DB_PATH)

@pytest.fixture
def completion_tracker():
    """Fixture to provide a Completion instance connected to the test database."""
    return Completion(DB_PATH)

# Utility function to create tables

# Tests

def test_add_habit(habit_tracker):
    """Test adding a new habit."""
    habit_tracker.add_habit("Test Habit", "A test habit", "daily")
    with sqlite3.connect(DB_PATH) as db:
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
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM completions WHERE habit_id = (SELECT id FROM habits WHERE name = 'Read Book')")
        completion = cursor.fetchone()
    assert completion is not None, "Completion should have been recorded for 'Read Book'"


def test_check_habits():
    """Test checking for broken habits with fixed completion patterns."""
    broken_habits = check_all_broken_habits()

    # Define expected broken habit messages based on the test completion data
    expected_broken_habits = [
        #"Habit 'Read Book' (Daily) is broken; last completed 2 days ago.",
        "Habit 'Exercise' (Daily) is broken; last completed 2 days ago.",
        "Habit 'Meditate' (Daily) is broken; last completed 2 days ago.",
        "Habit 'Weekly Review' (Weekly) is broken; last completed 2 weeks ago.",
        "Habit 'Clean House' (Weekly) is broken; last completed 2 weeks ago."
    ]

    # Check that each expected message appears in the actual broken habits
    for expected_message in expected_broken_habits:
        assert any(expected_message in habit for habit in broken_habits), \
            f"Expected broken habit message not found: {expected_message}"

    # Ensure no additional unexpected broken habits are detected
    assert len(broken_habits) == len(expected_broken_habits), "Unexpected broken habits found."


def test_list_habits():
    """Test listing all habits."""
    # Call get_all_habits and store its output directly
    habits = get_all_habits()

    # Check if each example habit is listed
    expected_habits = ["Read Book", "Exercise", "Meditate", "Clean House", "Weekly Review"]
    for habit in expected_habits:
        assert any(habit.startswith(habit_name.split(":")[0]) for habit_name in habits), f"Habit '{habit}' should be listed in output."

def test_list_by_period():
    """Test listing habits by periodicity."""
    # Get daily habits by periodicity
    daily_habits = get_habits_by_periodicity("daily")

    # Verify that only daily habits are listed
    expected_daily_habits = ["Exercise", "Read Book", "Meditate"]
    for habit in expected_daily_habits:
        assert any(habit.startswith(habit_name.split(":")[0]) for habit_name in daily_habits), f"Daily habit '{habit}' should be listed."

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