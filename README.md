# Habit Tracker App

## 1. Features

- **Habit Management**: Add, update, and delete habits with descriptions, start and end dates.
- **Frequency Management**: Set different frequencies for habits such as daily, weekly, etc.
- **Check-Offs**: Mark habits as completed on specific dates.
- **Analysis**: Analyze habits to find the longest streaks and categorize habits by frequency.

## 2. Installation

1. Clone the repository.
2. Ensure you have Python 3.7+ installed.
3. Ensure you have SQLite3 installed.
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