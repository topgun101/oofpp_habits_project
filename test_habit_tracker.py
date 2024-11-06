import os
from db import init_db, DB_PATH  # Import the DB_PATH
import pytest
import sqlite3
from example_data import add_example_habits
from habit import Habit
from completion import Completion
from analytics import get_longest_streak, get_all_habits, get_habits_by_periodicity, check_all_broken_habits

@pytest.fixture(scope="session", autouse=True) # The fixture is configured to be executed automatically once per test run before all tests.
def setup_test_database():
    """
    Sets up a clean test database by deleting any existing `test.db` file,
    initializing new tables, and populating it with fixed test data.

    Ensures that each test run starts with the same database state.

    - DB_PATH: Path to the test database file.
    """
    db_exists = os.path.exists(DB_PATH)
    # remove existing test.db, if already existing
    if db_exists:
        os.remove('test.db')

    # initialise new fresh DB and add fixed example data
    with sqlite3.connect(DB_PATH) as db:
        init_db()  # initialise tables in the database
        add_example_habits(db, test_data=True)  # add fixed example data via test_data=True

@pytest.fixture
def habit_tracker():
    """
    Fixture to provide a Habit instance connected to the test database.
    (It minimizes redundant instantiation of Habit objects and
    ensures consistency and avoids potential connection issues.)

    Returns:
        Habit: An instance of the Habit class initialized with the test database path.
    """
    return Habit(DB_PATH)

@pytest.fixture
def completion_tracker():
    """
    Fixture to provide a Completion instance connected to the test database.
    (It minimizes redundant instantiation of Completion objects and
    ensures consistency and avoids potential connection issues.)

    Returns:
        Completion: An instance of the Completion class initialized with the test database path.
    """
    return Completion(DB_PATH)

# Tests

def test_add_habit(habit_tracker):
    """
    Tests adding a new habit to the database and verifies its existence.

    Parameters:
        habit_tracker (Habit): An instance of the Habit class.
    """
    habit_tracker.add_habit("Test Habit", "A test habit", "daily")
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM habits WHERE name = ?", ("Test Habit",))
        habit = cursor.fetchone()
    assert habit is not None, "Habit 'Test Habit' should have been added"

def test_prevent_duplicate_habit(habit_tracker, capsys):
    """
    Tests duplicate habit prevention by verifying that adding a habit
    with an existing name does not insert a duplicate.

    Parameters:
        habit_tracker (Habit): An instance of the Habit class.
        capsys (pytest fixture): Captures stdout/stderr during test.
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
    """
    Tests deleting a habit and verifies it no longer exists in the database.

    Parameters:
        habit_tracker (Habit): An instance of the Habit class.
    """
    habit_tracker.add_habit("Test Habit", "A test habit", "daily")
    habit_tracker.delete_habit("Test Habit")  # Delete the added habit

    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM habits WHERE name = ?", ("Test Habit",))
        habit = cursor.fetchone()
    assert habit is None, "Habit 'Test Habit' should have been deleted."

def test_add_completion(completion_tracker):
    """
    Tests adding a completion record for a habit and verifies its existence.

    Parameters:
        completion_tracker (Completion): An instance of the Completion class.
    """
    completion_tracker.add_completion("Read Book")
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM completions WHERE habit_id = (SELECT id FROM habits WHERE name = 'Read Book')")
        completion = cursor.fetchone()
    assert completion is not None, "Completion should have been recorded for 'Read Book'"


def test_check_habits():
    """
    Tests checking for broken habits by verifying the output matches
    expected patterns based on fixed completion data.

    Expected Output:
        - A list of messages identifying specific broken habits.
    """
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
    """
    Tests listing all habits to verify that each example habit is correctly listed.

    Expected Output:
        - A list of habit names that should include specific test data.
    """
    # Call get_all_habits and store its output directly
    habits = get_all_habits()

    # Check if each example habit is listed
    expected_habits = ["Read Book", "Exercise", "Meditate", "Clean House", "Weekly Review"]
    for habit in expected_habits:
        assert any(habit.startswith(habit_name.split(":")[0]) for habit_name in habits), f"Habit '{habit}' should be listed in output."

def test_list_by_period():
    """
    Tests listing habits by their periodicity and verifies that only
    habits with the specified periodicity are listed.

    Expected Output:
        - A list of habits with "daily" periodicity.
    """
    # Get daily habits by periodicity
    daily_habits = get_habits_by_periodicity("daily")

    # Verify that only daily habits are listed
    expected_daily_habits = ["Exercise", "Read Book", "Meditate"]
    for habit in expected_daily_habits:
        assert any(habit.startswith(habit_name.split(":")[0]) for habit_name in daily_habits), f"Daily habit '{habit}' should be listed."

def test_longest_streak_for_specific_habit(habit_tracker, completion_tracker):
    """
    Tests calculating the longest streak for a specific habit.

    Parameters:
        habit_tracker (Habit): An instance of the Habit class.
        completion_tracker (Completion): An instance of the Completion class.

    Expected Output:
        - A streak result for the specified habit "Read Book".
    """
    longest_streaks = get_longest_streak("Read Book")

    # There should be at least one result
    assert longest_streaks, "Expected at least one longest streak for 'Read Book'"

    # Check each entry in the returned longest streaks list
    for habit, streak, period_type in longest_streaks:
        assert habit == "Read Book", "The habit name should be 'Read Book'"
        assert streak >= 1, "The streak for 'Read Book' should be at least 1 day"
        assert period_type == "days", "The period type should be 'days' for a daily habit"

def test_longest_streak_across_all_habits(habit_tracker, completion_tracker):
    """
    Tests calculating the longest streak across all tracked habits.

    Parameters:
        habit_tracker (Habit): An instance of the Habit class.
        completion_tracker (Completion): An instance of the Completion class.

    Expected Output:
        - A list of longest streaks for all tracked habits.
    """
    longest_streaks = get_longest_streak()

    # There should be at least one result
    assert longest_streaks, "Expected at least one longest streak across all habits"

    # Define a list of valid tracked habits
    tracked_habits = ["Read Book", "Exercise", "Meditate", "Clean House", "Weekly Review"]

    # Verify conditions for each habit with the longest streak
    for habit, streak, period_type in longest_streaks:
        assert habit in tracked_habits, \
            f"The habit with the longest streak should be one of the tracked habits, found: '{habit}'"
        assert streak >= 1, "The longest streak should be at least 1"
        assert period_type in ["days", "weeks"], "The period type should be either 'days' or 'weeks'"
