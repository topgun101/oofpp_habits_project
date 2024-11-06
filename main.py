import click
from db import init_db, DB_PATH  # Import the DB_PATH and initialze function for the DB
from habit import Habit
from completion import Completion
from analytics import get_all_habits, get_habits_by_periodicity, get_longest_streak, check_all_broken_habits

# Create instances of the Habit and Completion classes
habit = Habit(DB_PATH)
completion = Completion(DB_PATH)

class OrderedGroup(click.Group):
    """A custom Group class to preserve command order in the menu."""
    def list_commands(self, ctx):
        return self.commands.keys()

# Initialize the CLI group with OrderedGroup
@click.group(cls=OrderedGroup)
def cli():
    """Habit Tracker CLI"""
    pass

@cli.command()
@click.argument('name')
@click.option('--description', default="", help='A brief description of the habit.')
@click.argument('periodicity')
def add_habit(name, description, periodicity):
    """
    Add a new habit.

    :param name: The name of the habit.
    :param description: A description of the habit.
    :param periodicity: 'daily' or 'weekly'.
    """
    habit.add_habit(name, description, periodicity)


@cli.command()
@click.argument('name')
def delete_habit(name):
    """
    Delete an existing habit.

    :param name: The name of the habit to delete.
    """
    habit.delete_habit(name)


@cli.command()
@click.argument('name')
def complete_habit(name):
    """
    Mark a habit as completed.

    :param name: The name of the habit to complete.
    """
    completion.add_completion(name)

@cli.command()
def list_habits():
    """Lists all current habits."""
    habits = get_all_habits()
    if habits:
        click.echo("Current Habits:")
        for habit in habits:
            click.echo(f"- {habit}")
    else:
        click.echo("No habits found.")

@cli.command()
@click.argument('periodicity')
def list_by_period(periodicity):
    """Lists habits with a specified periodicity."""
    habits = get_habits_by_periodicity(periodicity)
    if habits:
        click.echo(f"Habits with {periodicity.capitalize()} periodicity:")
        for habit in habits:
            click.echo(f"- {habit}")
    else:
        click.echo(f"No habits found with {periodicity} periodicity.")

@cli.command()
@click.option('--habit-name', help="Name of the habit to check the longest streak for.")
def longest_streak(habit_name):
    """Show the longest streak for a specific habit or all habits."""
    longest_streaks = get_longest_streak(habit_name)

    if longest_streaks:
        for habit, streak, period_type in longest_streaks:
            print(f"The longest streak for habit '{habit}' is {streak} {period_type}, without interruption.")
    else:
        if habit_name:
            print(f"No streak found for habit '{habit_name}'.")
        else:
            print("No streaks found for any habits.")

@cli.command()
def check_habits():
    """Check if any habits are broken."""
    broken_habits = check_all_broken_habits()

    if broken_habits:
        for message in broken_habits:
            print(message)
    else:
        print("All habits are up to date and not broken.")


if __name__ == '__main__':
    init_db()
    cli()