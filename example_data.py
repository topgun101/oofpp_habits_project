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
    Adds completion data for a habit over a period of 4 weeks with a fixed pattern.

    For daily habits, this will create a pattern where the habit is completed 6 days out of 7,
    ensuring a specific day (like the 7th day) is skipped.
    For weekly habits, it will add completions every other week to ensure some weeks are missed.
    """
    cursor = db.cursor()
    today = datetime.now().date()

    if periodicity == 'daily':
        # For daily habits, skip every 7th day to simulate a missed day
        for day in range(28):  # 4 weeks
            completion_date = today - timedelta(days=day)
            if day % 7 != 0:  # Complete every day except the 7th day
                cursor.execute(
                    'INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)',
                    (habit_id, completion_date)
                )

    elif periodicity == 'weekly':
        # For weekly habits, complete every other week
        for week in range(4):
            if week % 2 == 0:  # Complete every second week
                completion_date = today - timedelta(weeks=week)
                cursor.execute(
                    'INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)',
                    (habit_id, completion_date)
                )

    db.commit()

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
        print(f"Added habit: {habit['name']}")  # Debugging output

        habit_id = cursor.lastrowid

        # Add either test or standard completion data
        if test_data:
            add_test_example_completions(db, habit_id, habit["periodicity"])
        else:
            add_example_completions(db, habit_id, habit["periodicity"])