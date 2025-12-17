import os
from .logger import sys_logger

class SecurityTools:
    def secure_shred(self, filepath, passes=3):
        if not os.path.exists(filepath): return False 
        try:
            size = os.path.getsize(filepath)
            with open(filepath, "ba+") as f:
                for i in range(passes):
                    f.seek(0)
                    f.write(os.urandom(size))
            os.remove(filepath)
            sys_logger.log(f"Secure Deleted: {os.path.basename(filepath)}", "WARNING")
            return True
        except Exception as e:
            sys_logger.log(f"Shred Error: {e}", "ERROR")
            return False

    def nuke_folder(self, folder_path):
        sys_logger.log(f"Starting Recursive Deletion: {folder_path}", "WARNING")
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for name in files:
                self.secure_shred(os.path.join(root, name), passes=1)
            for name in dirs:
                try: os.rmdir(os.path.join(root, name))
                except: pass
        try: os.rmdir(folder_path)
        except: pass
        sys_logger.log("Folder Deletion Complete.", "INFO")
