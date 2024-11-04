import sqlite3
from datetime import datetime, timedelta

def add_example_completions(db, habit_id, periodicity):
    """
    Adds example completion data for a habit over a period of 4 weeks.

    For daily habits, add completions for most days.
    For weekly habits, add completions for each week.
    """
    cursor = db.cursor()
    today = datetime.now()
    if periodicity == 'daily':
        # Simulate daily habit completions for 4 weeks (some days missed)
        for day in range(28):  # 4 weeks
            completion_date = today - timedelta(days=day)
            # Simulate missing a few days for variation
            if day % 7 != 0:  # Miss one day per week to simulate a break
                cursor.execute('INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)',
                               (habit_id, completion_date))
    elif periodicity == 'weekly':
        # Simulate weekly habit completions for the past 4 weeks
        for week in range(4):
            completion_date = today - timedelta(weeks=week)
            cursor.execute('INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)',
                           (habit_id, completion_date))

    db.commit()

def add_example_habits(db):
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

        # Add example completion data for the past 4 weeks
        add_example_completions(db, habit_id, habit["periodicity"])