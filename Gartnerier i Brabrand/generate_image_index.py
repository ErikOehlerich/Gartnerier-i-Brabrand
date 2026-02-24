import os
import json
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Billedformater vi leder efter
image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.tif', '.tiff', '.bmp', '.webp']

# Dictionary til at holde alle billeder/filer
image_index = {}

# Funktion til at konvertere TIF til JPEG
def convert_tif_to_jpg(tif_path):
    try:
        jpg_path = os.path.splitext(tif_path)[0] + '_converted.jpg'
        if not os.path.exists(jpg_path):
            img = Image.open(tif_path)
            # Konverter til RGB hvis nødvendigt
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(jpg_path, 'JPEG', quality=90)
            print(f"Konverteret: {tif_path} -> {jpg_path}")
        return os.path.basename(jpg_path)
    except Exception as e:
        print(f"Fejl ved konvertering af {tif_path}: {e}")
        return None

# Funktion til at liste billeder og filer i en mappe
def list_punkt_files(folder_path):
    images = []
    files = []
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            full_path = os.path.join(folder_path, filename)
            if not os.path.isfile(full_path):
                continue
            file_lower = filename.lower()
            if any(file_lower.endswith(ext) for ext in image_extensions):
                # Hvis det er en TIF-fil, konverter den
                if file_lower.endswith('.tif') or file_lower.endswith('.tiff'):
                    converted_name = convert_tif_to_jpg(full_path)
                    if converted_name:
                        images.append(converted_name)
                else:
                    images.append(filename)
            else:
                files.append(filename)
    unique_images = sorted(set(images), key=lambda s: s.lower())
    unique_files = sorted(set(files), key=lambda s: s.lower())
    return unique_images, unique_files

punkt_dirs = []
for name in os.listdir(BASE_DIR):
    lower = name.lower()
    if lower.startswith('punkt'):
        num_str = lower.replace('punkt', '', 1)
        if num_str.isdigit():
            punkt_dirs.append((int(num_str), name))

for punkt_nr, punkt_name in sorted(punkt_dirs, key=lambda x: x[0]):
    folder_path = os.path.join(BASE_DIR, punkt_name)
    images, files = list_punkt_files(folder_path)
    image_index[str(punkt_nr)] = {
        "images": images,
        "files": files
    }

# Gem til JSON-fil
with open('punkt_index.json', 'w', encoding='utf-8') as f:
    json.dump(image_index, f, ensure_ascii=False, indent=2)

print(f"Punkt index genereret med {len(image_index)} mapper")
print("Fil gemt som: punkt_index.json")
