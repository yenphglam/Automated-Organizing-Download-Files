import os
import re

DOWNLOADS_DIR = os.path.expanduser("~/Downloads")

DUPLICATE_PATTERN = re.compile(r"^(.*?)\s*\(\d+\)(\.[^.]+)?$")

def clean_existing_duplicates() : 
    files = sorted(os.listdir(DOWNLOADS_DIR))
    
    for filename in files:
        match = DUPLICATE_PATTERN.match(filename)
        
        if match: 
            base_name = match.group(1) # base_name get the actual name before adding numbers, such as file(1).pdf - it only file.pdf
            extension = match.group(2) or "" # extract extension part ".pdf", ".docx" - if nothing, it return "" (nothing)
            original_filename = f"{base_name}{extension}"
            
            duplicate_path = os.path.join(DOWNLOADS_DIR, filename)
            original_path = os.path.join(DOWNLOADS_DIR, original_filename)
            
            if os.path.exists(original_path) :
                os.remove(original_path)
                print(f"Removed old '{original_filename}'")
                
                os.rename(duplicate_path, original_path)
                print(f"Renamed '{filename}' to '{original_filename}'")
                
if __name__ == "__main__":
    print(f"Scanning '{DOWNLOADS_DIR}' for existing duplicates...")
    clean_existing_duplicates()
    print("Cleanup complete!")