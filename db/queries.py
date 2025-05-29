CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS buys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    purchase TEXT NOT NULL,
    bought INTEGER DEFAULT 0
    )
"""

SELECTS = "SELECT id, purchase, bought FROM buys"
INSERTS = "INSERT INTO buys (purchase) VALUES (?)"
DELETE = "DELETE FROM buys WHERE id = ?"
SELECT_BOUGHT = "SELECT id, purchase, bought FROM buys WHERE bought = 1"
SELECT_NOT_BOUGHT = "SELECT id, purchase, bought FROM buys WHERE bought = 0"