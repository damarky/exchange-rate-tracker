import logging
import sqlite3

import requests

logging.basicConfig(
    filename='pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

DATABASE_NAME = 'rates.db'
logging.info(f"Connecting to {DATABASE_NAME}")
conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()

logging.info("Creating DB if it does not exist.")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS rates (
        date TEXT NOT NULL, 
        base_currency TEXT NOT NULL, 
        target_currency TEXT NOT NULL,
        rate REAL NOT NULL,
        pct_change REAL,
        PRIMARY KEY (date, base_currency, target_currency)
    )
    """)

conn.commit()

logging.info("Starting fetch run")
try:
    response = requests.get("https://api.frankfurter.dev/v1/latest?base=USD&symbols=JPY,PHP")
except requests.exceptions.RequestException as e:
    logging.error(f"Request failed: {e}")
    exit()

if response.status_code != 200:
    logging.error(f"Request failed with status {response.status_code}")
    exit()

data = response.json()

current_date = data['date']
base_currency = data['base']
logging.info(f"Fetched {len(data['rates'])} currency rates")

for key, value in data['rates'].items():
    
    target_currency = key
    new_rate = value

    cursor.execute("""
        SELECT date, rate
        FROM rates
        WHERE base_currency= ? AND target_currency = ? AND date <> ?
        ORDER BY date DESC
        LIMIT 1;
        """,
        (base_currency, target_currency, current_date)
    )
    result = cursor.fetchone()
    if result:
        old_rate = result[1]
        pct_change = (new_rate - old_rate) / old_rate * 100
    else:
        pct_change = None
        logging.warning(f"No previous date found for {target_currency}")
    cursor.execute(
        "INSERT OR IGNORE INTO rates (date, base_currency, target_currency, rate, pct_change) VALUES (?, ?, ?, ?, ?)",
        (current_date, base_currency, target_currency, new_rate, pct_change)
    )

conn.commit()
conn.close()
logging.info("Fetch run completed successfully")