import os
import shutil
import json
import time
import hashlib
import zipfile
from .logger import sys_logger

SETTINGS_FILE = "settings.json"

class CleanerEngine:
    def __init__(self):
        self.rules = self.load_rules()

    def load_rules(self):
        default_rules = {
            ".jpg": "Images", ".jpeg": "Images", ".png": "Images", ".gif": "Images",
            ".mp4": "Videos", ".mkv": "Videos", ".mov": "Videos",
            ".pdf": "Documents", ".docx": "Documents", ".txt": "Documents",
            ".exe": "Installers", ".msi": "Installers",
            ".zip": "Archives", ".rar": "Archives"
        }
        if not os.path.exists(SETTINGS_FILE):
            return default_rules
        try:
            with open(SETTINGS_FILE, 'r') as f: return json.load(f)
        except: return default_rules

    def save_rules(self, new_rules):
        with open(SETTINGS_FILE, 'w') as f: json.dump(new_rules, f, indent=4)
        self.rules = new_rules

    def generate_unique_name(self, destination, filename):
        name, ext = os.path.splitext(filename)
        counter = 1
        new_path = os.path.join(destination, filename)
        while os.path.exists(new_path):
            new_filename = f"{name}_({counter}){ext}"
            new_path = os.path.join(destination, new_filename)
            counter += 1
        return new_path

    def process_file(self, filepath):
        if not os.path.exists(filepath): return
        filename = os.path.basename(filepath)
        if filename.startswith('.') or filename.endswith('.tmp'): return

        name, ext = os.path.splitext(filename)
        dest_folder_name = self.rules.get(ext.lower(), "Others")
        
        base_dir = os.path.dirname(filepath)
        dest_dir = os.path.join(base_dir, dest_folder_name)

        if not os.path.exists(dest_dir): 
            try: os.makedirs(dest_dir)
            except: return

        final_path = self.generate_unique_name(dest_dir, filename)

        try:
            shutil.move(filepath, final_path)
            sys_logger.log(f"Moved: {filename} -> {dest_folder_name}", "ACTION")
        except Exception as e:
            sys_logger.log(f"Move Failed: {e}", "ERROR")

    def scan_folder(self, target_dir):
        sys_logger.log(f"Scanning: {target_dir}", "ACTION")
        if not os.path.exists(target_dir):
            sys_logger.log("Directory not found.", "ERROR")
            return
            
        count = 0
        try:
            for item in os.listdir(target_dir):
                full_path = os.path.join(target_dir, item)
                if os.path.isfile(full_path):
                    self.process_file(full_path)
                    count += 1
            sys_logger.log(f"Scan complete. Sorted {count} files.", "INFO")
        except Exception as e:
            sys_logger.log(f"Error: {e}", "ERROR")

    def reverse_cleaning(self, target_dir):
        sys_logger.log(f"Reversing folder structure: {target_dir}", "WARNING")
        moved_count = 0
        for root, dirs, files in os.walk(target_dir, topdown=False):
            if root == target_dir: continue 
            for name in files:
                src = os.path.join(root, name)
                base, ext = os.path.splitext(name)
                dst = os.path.join(target_dir, name)
                c = 1
                while os.path.exists(dst):
                    dst = os.path.join(target_dir, f"{base}_restored_{c}{ext}")
                    c += 1
                try:
                    shutil.move(src, dst)
                    moved_count += 1
                except: pass
            
            try: os.rmdir(root)
            except: pass
        sys_logger.log(f"Reverse complete. Flattened {moved_count} files.", "INFO")

    def find_duplicates(self, target_dir):
        hashes = {}
        duplicates = []
        sys_logger.log("Scanning for duplicates...", "INFO")
        for root, dirs, files in os.walk(target_dir):
            for filename in files:
                path = os.path.join(root, filename)
                try:
                    with open(path, 'rb') as f:
                        file_hash = hashlib.md5(f.read(4096)).hexdigest()
                    if file_hash in hashes: duplicates.append(path)
                    else: hashes[file_hash] = path
                except: pass
        return duplicates

    def archive_old_files(self, target_dir, days=30):
        cutoff = time.time() - (days * 86400)
        archive_name = os.path.join(target_dir, f"Archive_{int(time.time())}.zip")
        files_to_zip = []
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                path = os.path.join(root, file)
                try:
                    if os.path.getmtime(path) < cutoff and not file.endswith('.zip'):
                        files_to_zip.append(path)
                except: pass

        if not files_to_zip: return
        sys_logger.log(f"Archiving {len(files_to_zip)} files...", "ACTION")
        try:
            with zipfile.ZipFile(archive_name, 'w') as zipf:
                for file in files_to_zip:
                    zipf.write(file, os.path.basename(file))
                    os.remove(file)
            sys_logger.log(f"Archive Created: {archive_name}", "INFO")
        except: pass
