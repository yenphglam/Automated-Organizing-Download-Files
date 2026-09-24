import os
import re
import time
from watchdog.observers import Observer # continuously watches designated directory & handle the lifecycle
from watchdog.events import FileSystemEventHandler

DOWNLOADS_DIR = os.path.expanduser("~/Downloads")

DUPLICATE_PATTERN = re.compile(r"^(.*?)\s*\(\d+\)(\.[^.]+)?$")

class DuplicateFileHandler(FileSystemEventHandler):
    
    # We move the core logic into its own function so we can use it for creations, modifications, and renames
    def process_file(self, file_path):
        directory, filename = os.path.split(file_path)

        # Skip temporary files
        if filename.endswith(('.crdownload', '.part', '.tmp')):
            return

        match = DUPLICATE_PATTERN.match(filename)
        
        if match: 
            base_name = match.group(1) 
            extension = match.group(2) or "" 
            original_filename = f"{base_name}{extension}"
            original_path = os.path.join(directory, original_filename)
            
            # If both the original and the new duplicate exist...
            if os.path.exists(original_path) and os.path.exists(file_path):
                try:
                    # Wait exactly 1 second for the browser to finish writing
                    time.sleep(1) 
                    
                    # Delete the newly downloaded duplicate, keep the original!
                    os.remove(file_path)
                    
                    print(f"SUCCESS: Deleted duplicate '{filename}'. Kept original '{original_filename}'.")
                except Exception as e:
                    print(f"FAILED to remove '{filename}': {e}")

    # callback that automatically fires whenever a new file is created
    def on_created(self, event): 
        if not event.is_directory:   
            # watchdog provides a string containing the complete path to that file (event.src_path)
            self.process_file(event.src_path)

    # callback that fires when a browser renames .crdownload to the final file
    def on_moved(self, event):
        if not event.is_directory:
            self.process_file(event.dest_path)
            
    # callback that fires when an app does a final save/write
    def on_modified(self, event):
        if not event.is_directory:
            self.process_file(event.src_path)

if __name__ == "__main__":
    event_handler = DuplicateFileHandler()
    observer = Observer()
    
    observer.schedule(event_handler, DOWNLOADS_DIR, recursive=False)
    print(f"Monitoring '{DOWNLOADS_DIR}' for numbered duplicate downloads...")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()