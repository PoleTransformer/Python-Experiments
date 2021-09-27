import requests

response = requests.get("https://api.github.com/repos/chemplusplus/Chemplusplus/releases/latest")
print(response.json()["name"])