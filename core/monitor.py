import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .logger import sys_logger

class WatcherHandler(FileSystemEventHandler):
    def __init__(self, engine):
        self.engine = engine
    def on_created(self, event):
        if not event.is_directory:
            time.sleep(1)
            sys_logger.log(f"New file detected: {event.src_path}", "ACTION")
            self.engine.process_file(event.src_path)

class BackgroundMonitor:
    def __init__(self, engine):
        self.engine = engine
        self.observer = None
        self.is_running = False
    def start(self, path):
        if self.is_running: return
        try:
            event_handler = WatcherHandler(self.engine)
            self.observer = Observer()
            self.observer.schedule(event_handler, path, recursive=False)
            self.observer.start()
            self.is_running = True
            sys_logger.log("Auto-Monitor Started.", "INFO")
        except Exception as e: sys_logger.log(f"Monitor failed: {e}", "ERROR")
    def stop(self):
        if not self.is_running: return
        self.observer.stop()
        self.observer.join()
        self.is_running = False
        sys_logger.log("Auto-Monitor Stopped.", "INFO")
