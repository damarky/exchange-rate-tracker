import sqlite3

import requests

conn = sqlite3.connect('rates.db')
cursor = conn.cursor()

response = requests.get("https://api.frankfurter.dev/v1/latest?base=USD&symbols=JPY,PHP")

data = response.json()

date = data['date']
base_currency = data['base']

for key, value in data['rates'].items():
    target_currency = key
    rate = value
    cursor.execute(
        "INSERT OR IGNORE INTO rates (date, base_currency, target_currency, rate) VALUES (?, ?, ?, ?)",
        (date, base_currency, target_currency, rate)
    )

conn.commit()
conn.close()
