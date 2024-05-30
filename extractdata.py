import os
 
# Chemin vers votre dossier principalf
dossier_principal = "/content/drive/MyDrive/extracted_folders"
 
# Chemin vers le fichier où vous allez stocker les données prétraitées
fichier_dataset = "/content/donnees_pretraitees.txt"
 
# Marqueur spécial pour indiquer le début et la fin du code STEP
START_STEP_MARKER = "<START_STEP>"
END_STEP_MARKER = "<END_STEP>"
import os
 
def read_file(filepath):
    """Read the content of a file and return it as a string."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return ""
 
def extract_useful_description(description):
    """Extract only the relevant lines from the description."""
    useful_lines = []
    for line in description.split('\n'):
        if any(field in line for field in ['TraceParts.PartNumber', 'REFERENCE', 'TraceParts.PartTitle', 'DESIGN']):
            useful_lines.append(line)
    return '\n'.join(useful_lines)
 
def prepare_dataset(root_dir, output_file):
    """Prepare the dataset for training the language model."""
    with open(output_file, "w", encoding="utf-8") as dataset:
        for folder, _, files in os.walk(root_dir):
            txt_files = [file for file in files if file.endswith('.txt')]
            step_files = [file for file in files if file.endswith('.stp')]
            for txt_file, step_file in zip(txt_files, step_files):
                txt_path = os.path.join(folder, txt_file)
                step_path = os.path.join(folder, step_file)
                description = read_file(txt_path)
                step_code = read_file(step_path)
                if description and step_code:
                    useful_description = extract_useful_description(description)
                    dataset.write(f"Input: {useful_description}\n")
                    dataset.write(f"Output: {step_code}\n\n")
# Chemin vers votre dossier principal contenant les données
root_dir = dossier_principal
 
# Chemin vers le fichier où vous allez stocker la dataset préparée
output_file = fichier_dataset
 
# Préparer la dataset
prepare_dataset(root_dir, output_file)
 
print("Dataset préparée avec succès !")