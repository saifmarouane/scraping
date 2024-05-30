import json
import requests
from concurrent.futures import ThreadPoolExecutor
import zipfile
import os

# Lire le fichier JSON
with open('output.json', 'r') as file:
    data = json.load(file)

# Define a global directory for extracted folders
global_directory = "extracted_folders"
os.makedirs(global_directory, exist_ok=True)

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
        extract_zip(local_filename, label)
        os.remove(local_filename)  # Remove the ZIP file after extraction
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {label} from {url}: {e}")

# Fonction pour extraire un fichier ZIP
def extract_zip(zip_filename, label):
    folder_name = label.replace(" ", "_")  # Create a folder name from the label
    destination_path = os.path.join(global_directory, folder_name)
    os.makedirs(destination_path, exist_ok=True)
    try:
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(destination_path)
        print(f"Extracted {zip_filename} into folder {destination_path}")
    except zipfile.BadZipFile as e:
        print(f"Failed to extract {zip_filename}: {e}")

# Utiliser ThreadPoolExecutor pour télécharger les fichiers en parallèle
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(download_file, data)