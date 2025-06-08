CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    added_date TEXT
    )
"""

SELECTS = "SELECT id, task, completed, added_date FROM tasks"
INSERTS = "INSERT INTO tasks (task, added_date) VALUES (?, ?)"
DELETE = "DELETE FROM tasks WHERE id = ?"
SELECT_COMPLETED = "SELECT id, task, completed, added_date FROM tasks WHERE completed = 1"
SELECT_NOT_COMPLETED = "SELECT id, task, completed, added_date FROM tasks WHERE completed = 0"