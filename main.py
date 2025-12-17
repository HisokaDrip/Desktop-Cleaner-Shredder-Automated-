from ui.app import CleanSweepApp
import os
import sys

# Ensure proper pathing
sys.path.append(os.getcwd())

if __name__ == "__main__":
    if not os.path.exists("logs"):
        os.makedirs("logs")
        
    try:
        app = CleanSweepApp()
        app.mainloop()
    except KeyboardInterrupt:
        print("Shutting down.")
