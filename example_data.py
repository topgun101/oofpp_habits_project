import random
from datetime import datetime, timedelta

def add_example_completions(db, habit_id, periodicity):
    """
    Adds random completion data for a habit over a period of 4 weeks.

    For daily habits, randomly add completions for most days.
    For weekly habits, randomly add completions once per week or skip some weeks.
    """
    cursor = db.cursor()
    today = datetime.now()

    if periodicity == 'daily':
        # Simulate daily habit completions for 4 weeks with random days skipped
        for day in range(28):  # 4 weeks
            completion_date = today - timedelta(days=day)
            # Randomly decide whether to add a completion for each day
            if random.choice([True, False, True]):  # Higher chance of recording
                cursor.execute('INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)',
                               (habit_id, completion_date))

    elif periodicity == 'weekly':
        # Simulate weekly habit completions for the past 4 weeks with some random skips
        for week in range(4):
            completion_date = today - timedelta(weeks=week)
            # Randomly decide whether to add a completion for each week
            if random.choice([True, False]):  # 50% chance of recording
                cursor.execute('INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)',
                               (habit_id, completion_date))

    db.commit()


def add_test_example_completions(db, habit_id, periodicity):
    """
    Adds completion data for a habit over a period with fixed dates.

    For daily habits, completes each day except specific days to simulate missed completions.
    For weekly habits, completes every other week, leaving a 2-week gap to mark as broken.
    """
    cursor = db.cursor()
    today = (datetime.now() - timedelta(days=2)).date()  # Set the latest possible completion date to 2 days ago

    if periodicity == 'daily':
        # Complete every day except certain days, and stop 2 days before today
        for day in range(0, 28):
            completion_date = today - timedelta(days=day)
            if day not in {7, 14, 21}:  # Skip specific days to break the streak
                cursor.execute(
                    'INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)',
                    (habit_id, completion_date)
                )

    elif periodicity == 'weekly':
        # Complete every other week to ensure a two-week gap and stop at least one week before today
        for week in range(2, 8, 2):  # Avoid completing on the most recent week
            completion_date = today - timedelta(weeks=week)
            cursor.execute(
                'INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)',
                (habit_id, completion_date)
            )

def add_example_habits(db, test_data=False):
    """Adds 5 predefined example habits and related completion data."""
    habits = [
        {
            "name": "Read Book",
            "description": "Read at least 10 pages every night.",
            "periodicity": "daily"
        },
        {
            "name": "Exercise",
            "description": "30 minutes of physical exercise.",
            "periodicity": "daily"
        },
        {
            "name": "Weekly Review",
            "description": "Reflect on goals and achievements for the week.",
            "periodicity": "weekly"
        },
        {
            "name": "Clean House",
            "description": "Do a thorough cleaning of the house every week.",
            "periodicity": "weekly"
        },
        {
            "name": "Meditate",
            "description": "Meditate for 10 minutes every morning.",
            "periodicity": "daily"
        }
    ]

    for habit in habits:
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO habits (name, description, periodicity, created_at)
            VALUES (?, ?, ?, ?)
        ''', (habit["name"], habit["description"], habit["periodicity"], datetime.now()))

        habit_id = cursor.lastrowid

        # Add either test or standard completion data
        if test_data:
            add_test_example_completions(db, habit_id, habit["periodicity"])
        else:
            add_example_completions(db, habit_id, habit["periodicity"])