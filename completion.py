import sqlite3
from datetime import datetime
from db import DB_PATH  # Import the DB_PATH

class Completion:
    def __init__(self, db_path=DB_PATH):
        """
        Initialize the Completion class with a database path.
        """
        self.db_path = DB_PATH  # Use the imported DB_PATH

    def add_completion(self, habit_name):
        """
        Add a completion record for a given habit.

        :param habit_name: The name of the habit to mark as complete.
        """
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            # Retrieve habit ID
            cursor.execute("SELECT id FROM habits WHERE name = ?", (habit_name,))
            habit = cursor.fetchone()

            if not habit:
                print(f"Habit '{habit_name}' does not exist.")
                return

            habit_id = habit[0]
            completed_at = datetime.now().isoformat()  # Record completion in ISO format

            cursor.execute(
                '''
                INSERT INTO completions (habit_id, completed_at)
                VALUES (?, ?)
                ''',
                (habit_id, completed_at)
            )
            db.commit()
            print(f"Habit '{habit_name}' marked as complete at {completed_at}.")


    def get_completions(self, habit_id):
        """
        Retrieve all completion dates for a given habit ID as datetime.date objects.

        :param habit_id: ID of the habit to retrieve completions for.
        :return: List of completion dates as datetime.date objects.
        """
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute(
                '''
                SELECT completed_at FROM completions
                WHERE habit_id = ?
                ORDER BY completed_at DESC
                ''',
                (habit_id,)
            )
            # Parse each date to a datetime.date object and return a list of dates
            return [datetime.fromisoformat(row[0]).date() for row in cursor.fetchall()]