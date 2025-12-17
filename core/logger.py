import logging
import datetime
import os

class AppLogger:
    def __init__(self, log_file="logs/activity.log"):
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        self.log_file = log_file
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.gui_callback = None

    def set_gui_callback(self, callback_func):
        self.gui_callback = callback_func

    def log(self, message, level="INFO"):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] [{level}] {message}"
        
        if level == "INFO": logging.info(message)
        elif level == "ERROR": logging.error(message)
        elif level == "WARNING": logging.warning(message)

        # Professional Color Coding
        color = "#00ff00" # Green
        if level == "ERROR": color = "#ff5555" # Red
        if level == "WARNING": color = "#ffcc00" # Yellow
        if level == "ACTION": color = "#00E5FF" # Cyan

        if self.gui_callback:
            try:
                self.gui_callback(formatted_msg, color)
            except: pass
        else:
            print(formatted_msg)

sys_logger = AppLogger()
