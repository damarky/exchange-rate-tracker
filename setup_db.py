import sqlite3

conn = sqlite3.connect('rates.db')
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS rates (
        date TEXT NOT NULL, 
        base_currency TEXT NOT NULL, 
        target_currency TEXT NOT NULL,
        rate REAL NOT NULL, 
        PRIMARY KEY (date, base_currency, target_currency)
    )
    """)
conn.commit()
conn.close()