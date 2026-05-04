import urllib.request
import json

data = json.dumps({"location_name": "Oran", "user_language": "English"}).encode('utf-8')
req = urllib.request.Request('http://localhost:5000/api/ai-guide', data=data, headers={'Content-Type': 'application/json'})

try:
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    print("AI API Result:", result)
except Exception as e:
    print("API Error:", e)
