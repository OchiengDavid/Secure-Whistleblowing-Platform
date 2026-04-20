import subprocess
import os
from PIL import Image

def strip_metadata(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext in ['.jpg', '.jpeg', '.png', '.tiff']:
            img = Image.open(file_path)
            data = list(img.getdata())
            img_without_exif = Image.new(img.mode, img.size)
            img_without_exif.putdata(data)
            img_without_exif.save(file_path)
            return True
        else:
            result = subprocess.run(
                ['exiftool', '-all=', '-overwrite_original', file_path],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
    except Exception as e:
        print(f"Error scrubbing file: {e}")
        return False
