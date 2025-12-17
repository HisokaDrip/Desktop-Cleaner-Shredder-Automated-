import os
from .logger import sys_logger

class DiskAnalyzer:
    def __init__(self):
        self.filters = {
            "All Files (Hidden Included)": [],
            "Images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
            "Videos": ['.mp4', '.mkv', '.mov', '.avi', '.wmv'],
            "Documents": ['.pdf', '.docx', '.txt', '.xlsx', '.pptx'],
            "Archives": ['.zip', '.rar', '.7z', '.tar', '.gz'],
            "Executables": ['.exe', '.msi', '.bat', '.sh', '.bin']
        }

    def analyze_folder(self, folder_path, filter_mode="All Files (Hidden Included)"):
        file_list = []
        target_exts = self.filters.get(filter_mode, [])
        is_unlimited = (filter_mode == "All Files (Hidden Included)")
        
        sys_logger.log(f"Analyzing storage: {folder_path}...", "ACTION")
        
        for root, dirs, files in os.walk(folder_path):
            for name in files:
                if not is_unlimited:
                    _, ext = os.path.splitext(name)
                    if ext.lower() not in target_exts:
                        continue
                
                filepath = os.path.join(root, name)
                try:
                    size = os.path.getsize(filepath)
                    file_list.append((filepath, size))
                except: pass
        
        file_list.sort(key=lambda x: x[1], reverse=True)
        return file_list[:200]
    
    def format_size(self, size):
        power = 2**10
        n = 0
        power_labels = {0 : 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
        while size > power:
            size /= power
            n += 1
        return f"{size:.2f} {power_labels[n]}"
