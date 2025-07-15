import requests

url = "http://127.0.0.1:5000/register"
data = {"username": "amisha", "password": "test123"}

res = requests.post(url, json=data)
print(res.json())
