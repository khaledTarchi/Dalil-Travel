import urllib.request
import os

images = {
    # Location Cards (Actual Places)
    "tassili_location.jpg": "https://upload.wikimedia.org/wikipedia/commons/4/4b/Tassili_N%27Ajjer_National_Park_1.jpg",
    "brezina_location.jpg": "https://upload.wikimedia.org/wikipedia/commons/f/f5/La_mairie_Brezina_%D8%A8%D9%84%D8%AF%D9%8A%D8%A9_%D8%A8%D8%B1%D9%8A%D8%B2%D9%8A%D9%86%D8%A9.jpg",
    "timimoun_location.jpg": "https://upload.wikimedia.org/wikipedia/commons/c/ce/Entr%C3%A9e_de_Timimoun_%D8%AA%D9%8A%D9%85%D9%8A%D9%85%D9%88%D9%86.jpg",
    "djanet_location.jpg": "https://upload.wikimedia.org/wikipedia/commons/2/28/Djanet.jpg",
    
    # Guesthouses / Accommodations
    "tassili_guesthouse.jpg": "https://upload.wikimedia.org/wikipedia/commons/e/ec/Tassili_Najjer_%28Tuareg_camp%29.jpg",
    "brezina_guesthouse.jpg": "https://upload.wikimedia.org/wikipedia/commons/1/1a/Oasis_Brezina.jpg",
    "timimoun_guesthouse.jpg": "https://upload.wikimedia.org/wikipedia/commons/5/5a/Ksar_timimoun.jpg",
    "djanet_guesthouse.jpg": "https://upload.wikimedia.org/wikipedia/commons/0/02/Bivouac_Tadrart_Rouge.jpg",
    
    # Ad Image (Banana)
    "ad_banana.jpg": "https://upload.wikimedia.org/wikipedia/commons/8/8a/Banana-Single.jpg"
}

output_dir = os.path.join("app", "static", "img")
os.makedirs(output_dir, exist_ok=True)

req_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

for filename, url in images.items():
    filepath = os.path.join(output_dir, filename)
    print(f"Downloading {filename} from {url}...")
    try:
        req = urllib.request.Request(url, headers=req_headers)
        with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Success: {filename}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
