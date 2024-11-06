import click
from db import init_db, DB_PATH  # Import the DB_PATH and initialze function for the DB
from habit import Habit
from completion import Completion
from analytics import get_all_habits, get_habits_by_periodicity, get_longest_streak, check_all_broken_habits

# Create instances of the Habit and Completion classes
habit = Habit(DB_PATH)
completion = Completion(DB_PATH)

class OrderedGroup(click.Group):
    """
    A custom Group class to preserve command order in the CLI menu.

    Inherits from `click.Group` and overrides `list_commands` to
    display commands in the order they were added to the CLI group.
    """
    def list_commands(self, ctx):
        return self.commands.keys()

# Initialize the CLI group with OrderedGroup
@click.group(cls=OrderedGroup)
def cli():
    """Main entry point for the Habit Tracker CLI."""
    pass

@cli.command()
@click.argument('name')
@click.option('--description', default="", help='A brief description of the habit.')
@click.argument('periodicity')
def add_habit(name, description, periodicity):
    """
    Add a new habit to the tracker.

    :param name: The name of the habit.
    :param description: Optional. A brief description of the habit.
    :param periodicity: Specifies the frequency of the habit ('daily' or 'weekly').
    """
    habit.add_habit(name, description, periodicity)


@cli.command()
@click.argument('name')
def delete_habit(name):
    """
    Deletes an existing habit from the DB.

    :param name: The name of the habit to delete.
    """
    habit.delete_habit(name)


@cli.command()
@click.argument('name')
def complete_habit(name):
    """
    Mark a habit as completed.

    :param name: The name of the habit to mark as complete for the current date.
    """
    completion.add_completion(name)

@cli.command()
def list_habits():
    """
    List all current habits being tracked.

    Displays all tracked habits along with their descriptions.
    """
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
    """
    List habits by specified periodicity.

    :param periodicity: The periodicity of habits to list ('daily' or 'weekly').
    Displays habits with the given frequency.
    """
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
    """
    Show the longest streak of completions for a specific habit or all habits.

    :param habit_name: Optional. Name of a specific habit to display the longest streak for.
                       If omitted, shows the longest streak across all habits.
    """
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
    """
    Check if any habits are currently broken (missed the required periodic completion).

    Displays a message for each broken habit, showing the time since it was last completed.
    """
    broken_habits = check_all_broken_habits()

    if broken_habits:
        for message in broken_habits:
            print(message)
    else:
        print("All habits are up to date and not broken.")


if __name__ == '__main__':
    init_db()
    cli()