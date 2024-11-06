import sqlite3
from datetime import datetime, timedelta
from completion import Completion
from db import DB_PATH  # Import the DB_PATH

completion_tracker = Completion(DB_PATH)  # Create instance of Completion

def get_all_habits():
    """
    Retrieve a list of all habits with their descriptions.

    :return: List of strings in the format "<habit_name>: <description>" for each habit.
    """
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute('SELECT name, description FROM habits')
        return [f"{row[0]}: {row[1]}" for row in cursor.fetchall()]

def get_habits_by_periodicity(periodicity: str):
    """
    Retrieve a list of habits with a specified periodicity, including their descriptions.

    :param periodicity: The periodicity of the habits to retrieve ("daily" or "weekly").
    :return: List of strings in the format "<habit_name>: <description>" for each habit with the specified periodicity.
    """
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute('SELECT name, description FROM habits WHERE periodicity = ?', (periodicity,))
        return [f"{row[0]}: {row[1]}" for row in cursor.fetchall()]


def get_longest_streak(habit_name=None):
    """
    Calculate the longest streak of completions for a specific habit or across all habits.

    :param habit_name: Optional; if provided, calculate the longest streak for this specific habit.
                       If not provided, calculates the longest streak across all habits.
    :return: List of tuples in the format [(habit_name, longest_streak, period_type)].
             period_type is "days" for daily habits and "weeks" for weekly habits.
    """
    longest_streak = 0
    longest_habits = []  # List to store all habits with the longest streak

    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()

        # If a specific habit name is provided, filter by it; otherwise, get all habits
        if habit_name:
            cursor.execute("SELECT id, name, periodicity FROM habits WHERE name = ?", (habit_name,))
            habits = cursor.fetchall()
            if not habits:
                print(f"Habit '{habit_name}' does not exist.")
                return []
        else:
            cursor.execute("SELECT id, name, periodicity FROM habits")
            habits = cursor.fetchall()

        for habit_id, habit_name, periodicity in habits:
            completions = completion_tracker.get_completions(habit_id)
            if not completions:
                continue  # Skip if there are no completions for this habit

            current_streak = 1
            period_days = 1 if periodicity == 'daily' else 7
            last_completion_date = completions[0]

            for completed_date in completions[1:]:
                # Check if the completion is within the expected period for the streak
                if (last_completion_date - completed_date).days == period_days:
                    current_streak += 1
                else:
                    current_streak = 1  # Reset the streak if there's a gap

                last_completion_date = completed_date

            # Update longest_streak and longest_habits based on current_streak
            if current_streak > longest_streak:
                longest_streak = current_streak
                longest_habits = [(habit_name, longest_streak, 'days' if periodicity == 'daily' else 'weeks')]
            elif current_streak == longest_streak:
                longest_habits.append((habit_name, current_streak, 'days' if periodicity == 'daily' else 'weeks'))

    return longest_habits

def check_all_broken_habits():
    """
    Check all tracked habits to identify any broken habits, those not completed within their required periodicity.

    :return: List of strings describing broken habits, including their names, periodicity, and how long ago they were last completed.
             If a habit has never been completed, it is also marked as broken.
    """
    broken_habits = []  # Clear the list at the start to avoid duplicates
    today = datetime.now().date()

    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute("SELECT id, name, periodicity FROM habits")
        habits = cursor.fetchall()

    for habit_id, habit_name, periodicity in habits:
        completions = completion_tracker.get_completions(habit_id)

        if completions:
            last_completion_date = completions[0]  # Get the most recent completion date
            period_delta = timedelta(days=1) if periodicity == "daily" else timedelta(weeks=1)

            # Check if the last completion date is outside the required period
            if today - last_completion_date > period_delta:
                days_or_weeks = (today - last_completion_date).days
                if periodicity == "daily":
                    broken_habits.append(f"Habit '{habit_name}' (Daily) is broken; last completed {days_or_weeks} days ago.")
                else:
                    weeks_broken = days_or_weeks // 7
                    broken_habits.append(f"Habit '{habit_name}' (Weekly) is broken; last completed {weeks_broken} weeks ago.")

        else:
            # Mark habit as broken if there are no completions
            if periodicity == "daily":
                broken_habits.append(f"Habit '{habit_name}' (Daily) has never been completed and is broken.")
            else:
                broken_habits.append(f"Habit '{habit_name}' (Weekly) has never been completed and is broken.")


    return broken_habits