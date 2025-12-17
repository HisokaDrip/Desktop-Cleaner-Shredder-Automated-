# ⚡ Automation Utility | By Mazy

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-cyan)

**A professional-grade desktop automation and forensics suite.**  
Organize your files, monitor downloads, analyze storage, and securely destroy sensitive data—all in one interface.

---

## 🚀 Key Features

### 📂 Organization & Automation
*   **Manual Sort (Clean Folder):** Instantly grabs every file in a messy directory and sorts them into logical sub-folders (e.g., `.jpg` → `Images`, `.pdf` → `Documents`).
*   **🤖 Auto-Pilot (Background Monitor):** Runs silently in the background. As soon as you download a file, it is detected and moved to the correct folder instantly.
*   **↩️ Reverse Protocol:** The "Undo" button. Pulls files out of sub-folders, dumps them back to the root, and cleans up empty directories.
*   **⚙️ Rules Editor:** Fully customizable logic. You decide where specific file extensions go.

### 🛡️ Security & Forensics
*   **📊 Disk Analyzer:** Scans drives to find the largest files (including hidden ones) to visualize storage usage.
*   **🔒 Secure Shredder:** Permanently destroys single files. Uses **DoD Standard 3-Pass Overwrite** to ensure data is unrecoverable by forensic tools.
*   **☢️ Mass Incineration:** Recursively shreds an entire folder and all sub-contents. **(Irreversible)**.

### 🧹 Maintenance
*   **Smart Archive:** Identifies files untouched for 30+ days and zips them to save space.
*   **Deduplicator:** Scans file hashes to find and remove exact duplicates.

---

## 🧠 Under the Hood (How it Works)

This application combines system-level operations with cryptographic security:

1.  **Sorting Logic:** Uses Python's `shutil` library to parse file MIME types and extensions against the dictionary defined in your **Rules Editor**.
2.  **Event Monitoring:** Utilizes the `watchdog` library to hook into Operating System file events. When the OS signals `FileCreated`, the app triggers the sorting engine immediately.
3.  **Cryptographic Shredding:** Standard deletion only removes the filename reference. This app:
    *   Opens the file in **Binary Mode**.
    *   Overwrites the physical sectors with **random binary noise** 3 times.
    *   Unlinks the file.
    *   *Result:* Original data is physically impossible to read.

---

## 🛠️ Installation & Usage

1.  **Install Dependencies:**
    ```bash
    pip install watchdog psutil
    ```

2.  **Run the Application:**
    ```bash
    python main.py
    ```

---

## ⚠️ Disclaimer

**Use the Shredder/Incinerator with caution.**
The secure deletion features are designed to prevent data recovery. Once a file or folder is incinerated, it cannot be recovered.

---
**© 2025 By Mazy**
