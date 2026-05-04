import urllib.request
import os

images = {
    "oran.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Oran_-_Algeria.jpg/800px-Oran_-_Algeria.jpg",
    "sahara.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Sahara_desert.jpg/800px-Sahara_desert.jpg",
    "tlemcen.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Mansourah_Tlemcen.jpg/800px-Mansourah_Tlemcen.jpg",
    "constantine.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Pont_Sidi_M%27Cid_Constantine.jpg/800px-Pont_Sidi_M%27Cid_Constantine.jpg"
}

os.makedirs('app/static/img', exist_ok=True)

for name, url in images.items():
    try:
        # User-agent header is sometimes required by Wikipedia
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(os.path.join('app/static/img', name), 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print(f"Successfully downloaded {name}")
    except Exception as e:
        print(f"Failed to download {name}: {e}")
