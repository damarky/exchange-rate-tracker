import sqlite3

import requests

conn = sqlite3.connect('rates.db')
cursor = conn.cursor()

response = requests.get("https://api.frankfurter.dev/v1/latest?base=USD&symbols=JPY,PHP")

data = response.json()

current_date = data['date']
base_currency = data['base']

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
    print(pct_change)
    cursor.execute(
        "INSERT OR IGNORE INTO rates (date, base_currency, target_currency, rate, pct_change) VALUES (?, ?, ?, ?, ?)",
        (current_date, base_currency, target_currency, new_rate, pct_change)
    )

conn.commit()
conn.close()
