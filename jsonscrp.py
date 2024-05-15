import json
import requests
from concurrent.futures import ThreadPoolExecutor

# Lire le fichier JSON
with open('output.json', 'r') as file:
    data = json.load(file)

# Fonction pour télécharger un fichier
def download_file(entry):
    url = entry["link"]
    label = entry.get("label_text", "unknown")
    local_filename = url.split("filename%3D%22")[-1].split("%22")[0] if "filename%3D%22" in url else "unknown.zip"
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded {label} as {local_filename}")
    except Exception as e:
        print(f"Failed to download {label} from {url}: {e}")

# Utiliser ThreadPoolExecutor pour télécharger les fichiers en parallèle
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(download_file, data)
