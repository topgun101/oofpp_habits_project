import sqlite3
from datetime import datetime
from db import DB_PATH  # Import the DB_PATH

class Habit:
    """
    A class to represent a habit with a task, periodicity, and description.

    Attributes:
    name (str): The name of the habit.
    periodicity (str): The periodicity of the habit, either 'daily' or 'weekly'.
    description (str): A description of the habit.
    created_at (datetime): The creation date of the habit.
    completed_dates (list): List of datetime objects representing when the habit was completed.
    """

    def __init__(self, db_path=DB_PATH):
        """
        Initialize the Habit class with a database path.
        """
        self.db_path = db_path

    def add_habit(self, name: str, description: str = "", periodicity: str = "daily"):
        """
        Add a new habit to the database.

        :param name: Name of the habit.
        :param description: A description of the habit.
        :param periodicity: The periodicity of the habit ('daily' or 'weekly').
        """
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            # Check if the habit already exists to prevent duplicates
            cursor.execute("SELECT id FROM habits WHERE name = ?", (name,))
            if cursor.fetchone():
                print(f"Habit '{name}' already exists.")
                return  # Exit if habit already exists

            # Insert the habit into the database
            cursor.execute(
                '''
                INSERT INTO habits (name, description, periodicity, created_at)
                VALUES (?, ?, ?, ?)
                ''',
                (name, description, periodicity, datetime.now().isoformat())
            )
            db.commit()
            print(f"Habit '{name}' with periodicity '{periodicity}' added. Task description: '{description}'")

    def delete_habit(self, name):
        """
        Delete a habit from the database by its name.

        :param name: Name of the habit to delete.
        """
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            # Find the habit by name
            cursor.execute("SELECT id FROM habits WHERE name = ?", (name,))
            habit_id = cursor.fetchone()

            if habit_id is None:
                print(f"Habit '{name}' does not exist.")
                return

            habit_id = habit_id[0]

            # Delete completions related to the habit
            cursor.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))

            # Delete the habit itself
            cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
            db.commit()
            print(f"Habit '{name}' and its completions have been deleted.")