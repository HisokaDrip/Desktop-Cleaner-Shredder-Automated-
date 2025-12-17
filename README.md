Thee Features

Manual Sort (Clean Folder):
Instantly grabs every file in a messy folder and sorts them into sub-folders (e.g., .jpg goes to "Images", .pdf goes to "Documents").
Reverse / Unsort:
The "Undo" button. It pulls all files out of the sub-folders and dumps them back into the main folder, then deletes the empty folders.
Auto-Monitor (Auto-Pilot):
Runs silently in the background. As soon as you download a file, it instantly moves it to the correct folder. You never have to organize manually again.
Rules Editor:
Lets you customize the sorting. You can tell the app: "Put all .mp4 files into a folder named My Movies."
Disk Analyzer:
Scans your drive to find the largest files (even hidden ones) so you can see what is eating up your storage space.
Secure Shredder (Single File):
Permanently destroys a specific file. It doesn't just delete it; it scrambles the data so hackers cannot recover it.
Mass Nuke (Folder Delete):
Warning: Recursively shreds an entire folder and everything inside it. Used for total data destruction.
Maintenance:
Archive: Zips files you haven't touched in 30 days to save space.
Dedupe: Finds and deletes duplicate files. 

How It Works (Under the Hood)
Sorting: It uses Python’s shutil library to read file extensions (like .png) and move them based on the dictionary defined in your Rules Editor.
Monitoring: It uses a library called watchdog. It hooks into the Operating System events. When Windows says "A file was created," your app wakes up and runs the sort function immediately.
Shredding: Standard deletion just removes the filename. Your app opens the file in "Binary Mode," overwrites the actual data with random noise (gibberish) 3 times (DoD Standard), and then deletes it. This makes the original data physically impossible to read.



Run Main.Py
