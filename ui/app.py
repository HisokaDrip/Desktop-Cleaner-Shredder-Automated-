import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import psutil
import os

from core.engine import CleanerEngine
from core.monitor import BackgroundMonitor
from core.logger import sys_logger
from core.analyzer import DiskAnalyzer
from core.security import SecurityTools

# --- THEME CONFIG ---
BG_COLOR = "#1e1e1e"
FG_COLOR = "#ffffff"
ACCENT_COLOR = "#0078d7" # Professional Blue
PANEL_COLOR = "#252526"

class CleanSweepApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Automation Utility | By Mazy")
        self.geometry("1000x750")
        self.configure(bg=BG_COLOR)
        
        # Modules
        self.engine = CleanerEngine()
        self.monitor = BackgroundMonitor(self.engine)
        self.analyzer = DiskAnalyzer()
        self.shredder = SecurityTools()
        
        # Variables
        self.target_folder = tk.StringVar(value=os.path.expanduser("~/Desktop"))
        self.filter_var = tk.StringVar(value="All Files (Hidden Included)")

        self.setup_styles()
        self.build_ui()
        
        sys_logger.set_gui_callback(self.append_log)
        self.running = True
        threading.Thread(target=self.update_stats, daemon=True).start()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("TFrame", background=BG_COLOR)
        style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
        style.configure("TNotebook.Tab", background=PANEL_COLOR, foreground="gray", padding=[20, 10], font=("Segoe UI", 10))
        style.map("TNotebook.Tab", background=[("selected", ACCENT_COLOR)], foreground=[("selected", "white")])
        
        style.configure("Header.TLabel", background=PANEL_COLOR, foreground="white", font=("Segoe UI", 16, "bold"))
        style.configure("Sub.TLabel", background=BG_COLOR, foreground="lightgray", font=("Segoe UI", 12))
        
        style.configure("Main.TButton", background=ACCENT_COLOR, foreground="white", borderwidth=0, font=("Segoe UI", 10))
        style.map("Main.TButton", background=[("active", "#005a9e")])
        
        style.configure("Warn.TButton", background="#d9534f", foreground="white", borderwidth=0, font=("Segoe UI", 10))
        style.map("Warn.TButton", background=[("active", "#c9302c")])

    def build_ui(self):
        # HEADER
        top = tk.Frame(self, bg=PANEL_COLOR, height=60, padx=20, pady=15)
        top.pack(fill=tk.X)
        tk.Label(top, text="Desktop Automation Tool", bg=PANEL_COLOR, fg="white", font=("Segoe UI", 18, "bold")).pack(side=tk.LEFT)
        tk.Label(top, text="By Mazy", bg=PANEL_COLOR, fg=ACCENT_COLOR, font=("Segoe UI", 12)).pack(side=tk.LEFT, padx=10, pady=(8,0))
        
        self.stats_lbl = tk.Label(top, text="CPU: 0% | RAM: 0%", bg=PANEL_COLOR, fg="gray", font=("Consolas", 10))
        self.stats_lbl.pack(side=tk.RIGHT)

        # NAV BAR
        nav = tk.Frame(self, bg=BG_COLOR, pady=20, padx=20)
        nav.pack(fill=tk.X)
        tk.Label(nav, text="Selected Folder:", bg=BG_COLOR, fg="gray").pack(anchor="w")
        inp = tk.Frame(nav, bg=BG_COLOR)
        inp.pack(fill=tk.X, pady=5)
        tk.Entry(inp, textvariable=self.target_folder, bg=PANEL_COLOR, fg="white", relief="flat", insertbackground="white").pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)
        ttk.Button(inp, text="Browse", style="Main.TButton", command=self.browse).pack(side=tk.LEFT, padx=(10,0))

        # TABS
        nb = ttk.Notebook(self)
        nb.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 1. Dashboard
        self.build_dashboard(nb)
        # 2. Tools
        self.build_tools(nb)
        # 3. Rules
        self.build_rules(nb)
        # 4. Logs
        self.build_logs(nb)

    def build_dashboard(self, nb):
        tab = ttk.Frame(nb)
        nb.add(tab, text="Dashboard")
        
        grid = tk.Frame(tab, bg=BG_COLOR)
        grid.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Left Col
        col1 = tk.Frame(grid, bg=BG_COLOR)
        col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        ttk.Label(col1, text="Organization", style="Sub.TLabel").pack(anchor="w", pady=10)
        ttk.Button(col1, text="Run Sort (Clean Folder)", style="Main.TButton", command=self.run_sort).pack(fill=tk.X, pady=5)
        ttk.Button(col1, text="Reverse / Unsort Folder", style="Warn.TButton", command=self.run_reverse).pack(fill=tk.X, pady=5)
        
        ttk.Label(col1, text="Monitoring", style="Sub.TLabel").pack(anchor="w", pady=(20, 10))
        self.btn_mon_start = ttk.Button(col1, text="Start Auto-Monitor", style="Main.TButton", command=self.start_mon)
        self.btn_mon_start.pack(fill=tk.X, pady=5)
        self.btn_mon_stop = ttk.Button(col1, text="Stop Monitor", style="Warn.TButton", command=self.stop_mon)
        self.btn_mon_stop.pack(fill=tk.X, pady=5)
        self.btn_mon_stop.state(['disabled'])

        # Right Col
        col2 = tk.Frame(grid, bg=BG_COLOR)
        col2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        ttk.Label(col2, text="Maintenance", style="Sub.TLabel").pack(anchor="w", pady=10)
        ttk.Button(col2, text="Archive Old Files (>30 Days)", style="Main.TButton", command=self.run_archive).pack(fill=tk.X, pady=5)
        ttk.Button(col2, text="Delete Duplicates", style="Warn.TButton", command=self.run_dedupe).pack(fill=tk.X, pady=5)

    def build_tools(self, nb):
        tab = ttk.Frame(nb)
        nb.add(tab, text="Tools & Security")
        
        split = tk.Frame(tab, bg=BG_COLOR)
        split.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Left: Analyzer
        left = tk.Frame(split, bg=BG_COLOR)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        ttk.Label(left, text="Disk Analyzer", style="Sub.TLabel").pack(anchor="w")
        
        opts = list(self.analyzer.filters.keys())
        ttk.OptionMenu(left, self.filter_var, opts[0], *opts).pack(fill=tk.X, pady=5)
        ttk.Button(left, text="Scan Files", style="Main.TButton", command=self.run_analyze).pack(fill=tk.X, pady=5)
        
        cols = ("Name", "Size")
        self.tree_an = ttk.Treeview(left, columns=cols, show='headings', height=10)
        self.tree_an.heading("Name", text="File Name")
        self.tree_an.heading("Size", text="Size")
        self.tree_an.column("Name", width=300)
        self.tree_an.pack(fill=tk.BOTH, expand=True, pady=10)

        # Right: Security
        right = tk.Frame(split, bg=PANEL_COLOR, padx=15, pady=15)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        ttk.Label(right, text="Secure Delete", background=PANEL_COLOR, foreground="white", font=("Segoe UI", 12)).pack(anchor="w")
        tk.Label(right, text="Standard: 3-Pass Overwrite", bg=PANEL_COLOR, fg="gray").pack(anchor="w", pady=5)
        
        ttk.Button(right, text="Shred Single File", style="Warn.TButton", command=self.shred_one).pack(fill=tk.X, pady=15)
        
        tk.Label(right, text="Mass Operations", bg=PANEL_COLOR, fg="white", font=("Segoe UI", 10, "bold")).pack(pady=(20,5))
        ttk.Button(right, text="Delete Entire Folder (Recursive)", style="Warn.TButton", command=self.nuke_folder).pack(fill=tk.X, pady=5)

    def build_rules(self, nb):
        tab = ttk.Frame(nb)
        nb.add(tab, text="Rules Editor")
        
        frame = tk.Frame(tab, bg=BG_COLOR, pady=15)
        frame.pack(fill=tk.BOTH, expand=True)

        # Inputs
        in_frame = tk.Frame(frame, bg=BG_COLOR)
        in_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(in_frame, text="Extension (.ext):", bg=BG_COLOR, fg="white").pack(side=tk.LEFT)
        self.ent_ext = tk.Entry(in_frame, width=10)
        self.ent_ext.pack(side=tk.LEFT, padx=5)
        
        tk.Label(in_frame, text="Folder Name:", bg=BG_COLOR, fg="white").pack(side=tk.LEFT)
        self.ent_fld = tk.Entry(in_frame, width=20)
        self.ent_fld.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(in_frame, text="Add Rule", style="Main.TButton", command=self.add_rule).pack(side=tk.LEFT, padx=10)
        ttk.Button(in_frame, text="Remove Selected", style="Warn.TButton", command=self.del_rule).pack(side=tk.LEFT)

        # Table
        cols = ("Ext", "Folder")
        self.tree_rules = ttk.Treeview(frame, columns=cols, show='headings')
        self.tree_rules.heading("Ext", text="Extension")
        self.tree_rules.heading("Folder", text="Destination Folder")
        self.tree_rules.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.refresh_rules()

    def build_logs(self, nb):
        tab = ttk.Frame(nb)
        nb.add(tab, text="Logs")
        self.log_text = tk.Text(tab, bg="black", fg="#00ff00", font=("Consolas", 9), state="disabled")
        self.log_text.pack(fill=tk.BOTH, expand=True)

    # --- LOGIC ---
    def refresh_rules(self):
        for i in self.tree_rules.get_children(): self.tree_rules.delete(i)
        for ext, folder in self.engine.rules.items():
            self.tree_rules.insert("", "end", values=(ext, folder))

    def add_rule(self):
        ext = self.ent_ext.get().strip().lower()
        folder = self.ent_fld.get().strip()
        if not ext.startswith('.'): ext = '.' + ext
        if ext and folder:
            self.engine.rules[ext] = folder
            self.engine.save_rules(self.engine.rules)
            self.refresh_rules()
            self.ent_ext.delete(0, tk.END)
            self.ent_fld.delete(0, tk.END)

    def del_rule(self):
        sel = self.tree_rules.selection()
        if sel:
            item = self.tree_rules.item(sel[0])
            ext = item['values'][0]
            del self.engine.rules[ext]
            self.engine.save_rules(self.engine.rules)
            self.refresh_rules()

    def run_sort(self): threading.Thread(target=self.engine.scan_folder, args=(self.target_folder.get(),)).start()
    def run_reverse(self): 
        if messagebox.askyesno("Confirm", "Undo sorting? This flattens folders."):
            threading.Thread(target=self.engine.reverse_cleaning, args=(self.target_folder.get(),)).start()
    
    def start_mon(self): 
        self.monitor.start(self.target_folder.get())
        self.btn_mon_start.state(['disabled'])
        self.btn_mon_stop.state(['!disabled'])
    def stop_mon(self):
        self.monitor.stop()
        self.btn_mon_start.state(['!disabled'])
        self.btn_mon_stop.state(['disabled'])

    def run_archive(self): threading.Thread(target=self.engine.archive_old_files, args=(self.target_folder.get(),)).start()
    def run_dedupe(self):
        dupes = self.engine.find_duplicates(self.target_folder.get())
        if dupes:
            if messagebox.askyesno("Duplicates", f"Found {len(dupes)}. Delete?"):
                for d in dupes: os.remove(d)
                messagebox.showinfo("Done", "Duplicates deleted.")
        else: messagebox.showinfo("Clean", "No duplicates.")

    def run_analyze(self):
        for i in self.tree_an.get_children(): self.tree_an.delete(i)
        data = self.analyzer.analyze_folder(self.target_folder.get(), self.filter_var.get())
        for p, s in data:
            self.tree_an.insert("", "end", values=(os.path.basename(p), self.analyzer.format_size(s)))

    def shred_one(self):
        f = filedialog.askopenfilename(initialdir=self.target_folder.get())
        if f and messagebox.askyesno("Secure Delete", f"Permanently delete {os.path.basename(f)}?"):
            threading.Thread(target=self.shredder.secure_shred, args=(f,)).start()

    def nuke_folder(self):
        f = self.target_folder.get()
        if messagebox.askyesno("MASS DELETE", f"WARNING: Delete ALL contents of {f}? Cannot be undone."):
            threading.Thread(target=self.shredder.nuke_folder, args=(f,)).start()

    def browse(self):
        f = filedialog.askdirectory()
        if f: self.target_folder.set(f)

    def append_log(self, msg, color):
        self.log_text.config(state='normal')
        self.log_text.tag_config(color, foreground=color)
        self.log_text.insert(tk.END, msg + "\n", color)
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def update_stats(self):
        while self.running:
            try:
                c = psutil.cpu_percent(1)
                r = psutil.virtual_memory().percent
                self.stats_lbl.config(text=f"CPU: {c}% | RAM: {r}%")
            except: break
