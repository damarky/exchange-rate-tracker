import requests

response = requests.get("https://api.frankfurter.dev/v1/latest?base=USD&symbols=JPY,PHP")
# print(response.status_code)
# print(response.json())
data = response.json()

for key, value in data['rates'].items():
    print(key, value)
print(data['base'])
print(data['date'])