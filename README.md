# Habit Tracker App

## Installation

1. Clone the repository.
2. Ensure you have Python 3.7+ installed.
3. Install dependencies:
   ```shell
   pip install -r requirements.txt

## Usage
Run the application:
```shell
python main.py
```
   
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
    
List all habits:
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

Show longest streak for a specific habit:
```shell
python main.py longest-streak --habit-name "Read Book"
```

Check for broken habit:
```shell
python main.py check-habits
```

## Test
Run unit tests using pytest:
```shell
pytest test_habit-tracker.py
```