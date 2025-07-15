import requests

# Replace this URL with your live backend URL if deployed
BASE_URL = "http://127.0.0.1:5000/login"

# Simulated new user
username = "admin"
password = "admin123"

res = requests.post(BASE_URL, json={"username": username, "password": password})

if res.status_code == 200:
    print("[✅] Login successful!")
    print("Token:", res.json()["token"])
else:
    print("[❌] Login failed:", res.json())
