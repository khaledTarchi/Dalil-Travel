import urllib.request
import json

try:
    req = urllib.request.urlopen('http://localhost:5000/api/destinations?lang=en')
    data = json.loads(req.read().decode())
    print("Destinations API OK:", len(data) > 0)
except Exception as e:
    print("API Error:", e)
