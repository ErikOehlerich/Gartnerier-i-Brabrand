import os
import json
from PIL import Image

# Stier til mapper
billeder_base = "Billeder_og_tegninger/Billeder"
plantegninger_base = "Billeder_og_tegninger/Plantegninger"

# Billedformater vi leder efter
image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.tif', '.tiff', '.bmp', '.webp']

# Dictionary til at holde alle billeder
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

# Funktion til at liste billeder i en mappe
def list_images(folder_path):
    images = []
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            file_lower = filename.lower()
            if any(file_lower.endswith(ext) for ext in image_extensions):
                # Hvis det er en TIF-fil, konverter den
                if file_lower.endswith('.tif') or file_lower.endswith('.tiff'):
                    converted_name = convert_tif_to_jpg(os.path.join(folder_path, filename))
                    if converted_name:
                        images.append(converted_name)
                else:
                    images.append(filename)
    return sorted(images)

# Scan alle mapper
for mappe_nr in range(2, 71):  # Fra Mappe 2 til Mappe 70 (inklusive)
    mappe_name = f"Mappe {mappe_nr}"
    
    billeder_path = os.path.join(billeder_base, mappe_name)
    plantegninger_path = os.path.join(plantegninger_base, mappe_name)
    
    billeder = list_images(billeder_path)
    plantegninger = list_images(plantegninger_path)
    
    image_index[str(mappe_nr)] = {
        "billeder": billeder,
        "plantegninger": plantegninger
    }

# Gem til JSON-fil
with open('image_index.json', 'w', encoding='utf-8') as f:
    json.dump(image_index, f, ensure_ascii=False, indent=2)

print(f"Image index genereret med {len(image_index)} mapper")
print("Fil gemt som: image_index.json")
