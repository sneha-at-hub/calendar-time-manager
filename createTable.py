import sqlite3

conn = sqlite3.connect(f'hours.db')
cur = conn.cursor()
print("Opened database successfully")


conn.execute('''CREATE TABLE IF NOT EXISTS hours (
    DATE TEXT NOT NULL,
    CATEGORY TEXT NOT NULL,
    HOURS REAL NOT NULL,
    EVENT_DESCRIPTION TEXT NOT NULL,
    EVENT_ID TEXT NOT NULL  -- Assuming EVENT_ID is a text field
);
''')
print("Table created successfully")