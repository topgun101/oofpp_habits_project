# Habit Tracker App
Github: https://github.com/topgun101/oofpp_habits_project

## 1. App Features

- **Habit Management**: Add and delete habits with task descriptions and periodicity.
- **Completion Tracking**: Mark habits as completed at the current date and time.
- **Analysis**: Analyze habits to find longest streaks over all or specific habits, 
overview of stored habits, filter the list by periods (daily or weekly habits) 
and check for broken habits
- **Testing**: Run automated test to check all functionalities easily

## 2. Installation

1. Ensure Python 3.7+ is installed. 
2. Ensure SQLite3 is installed. 
3. Clone the repository.
```shell
gh repo clone topgun101/oofpp_habits_project
```
4. Install dependencies:
```shell
pip install -r requirements.txt
```

## 3. Usage
### 3.1 Database configuration
Ensure DB_PATH is set to **DB_PATH = 'data.db'** in the **db.py** (not 'test.db'). 'test.db' is only required for running tests
with pytest. The 'data.db' provides example data with random completion dates.
<br>(the data.db contains all stored habits. If the db-file gets deleted it will be
initialized with example data on startup again)

### 3.2 Run the application:
```shell
python main.py
```

## 4. Command examples   
Add a habit:
```shell
python main.py add-habit "Read Book" "daily" --description "Read a chapter every night."
```

Delete a habit:
```shell
python main.py delete-habit "Read Book"
```

Complete a habit:
```shell
python main.py complete-habit "Read Book"
```
    
List all stored habits:
```shell
python main.py list-habits
```

List habits by periodicity:
```shell
python main.py list-by-period daily
```

Show longest streak over all habits:
```shell
python main.py longest-streak
```

Show longest run streak for a specific habit:
```shell
python main.py longest-streak --habit-name "Read Book"
```

Check for broken habits:
```shell
python main.py check-habits
```

## 5. Test
### 5.1 Database configuration
Before running the test command it is necessary to change the database path in the **db.py** 
<br>from DB_PATH = 'data.db' to **DB_PATH = 'test.db'** otherwise pytest will not work properly.

(The test.db provides example data with fixed completion dates for testing)

### 5.2 Run unit tests using pytest:
```shell
pytest test_habit_tracker.py
```