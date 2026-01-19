import os
import pandas as pd
import tkinter as tk  # HATA DÜZELTİLDİ: tk -> tkinter
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import webbrowser

# =================================================================
# PROJECT: DeepByte Auditor
# AUTHOR: gktrk363
# AUTHOR REPO: https://github.com/gktrk363/
# PROJECT REPO: https://github.com/gktrk363/deepbyte-auditor
# DESCRIPTION: Büyük ölçekli UE5 projeleri için statik arayüzlü, 
# profesyonel düzeyde disk denetleme ve analiz yazılımı.
# =================================================================

# --- DESIGN SYSTEM ---
CLR_BG = '#050505'
CLR_CARD = '#0f0f0f'
CLR_RED = '#e63946'
CLR_RED_DARK = '#9b1b30'
CLR_TEXT = '#ffffff'
CLR_SUB = '#808080'
PALETTE = ['#8a0303', '#c90000', '#ff1a1a', '#ff4d4d', '#ff8080']

class DeepByteAuditor:
    def __init__(self, root):
        self.root = root
        self.root.title("DeepByte Auditor // Final Build 2026.1")
        self.root.geometry("1100x750")
        self.root.configure(bg=CLR_BG)
        self.df = pd.DataFrame()
        self.root.iconbitmap('app_icon.ico')
        
        self.setup_styles()
        self.create_layout()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('default')
        
        # Mavi hatları engelleyen layout ayarı
        style.layout("TNotebook.Tab", [('Notebook.tab', {'sticky': 'nswe', 'children': [
            ('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children': [
                ('Notebook.label', {'side': 'top', 'sticky': ''})]})]})])
        
        style.configure("TNotebook", background=CLR_BG, borderwidth=0, highlightthickness=0)
        style.configure("TNotebook.Tab", background=CLR_CARD, foreground=CLR_SUB, 
                        padding=[25, 10], borderwidth=0, focuscolor=CLR_BG)
        
        # SEKME HOVER İPTAL
        style.map("TNotebook.Tab", 
                  background=[("selected", CLR_RED), ("active", CLR_CARD)], 
                  foreground=[("selected", CLR_TEXT), ("active", CLR_SUB)])
        
        # BAŞLIK HOVER İPTAL - BEYAZLAMA ENGELLENDİ
        style.configure("Treeview.Heading", background=CLR_BG, foreground=CLR_RED, 
                        font=('Segoe UI Bold', 10), borderwidth=0, relief='flat')
        style.map("Treeview.Heading", 
                  background=[('active', CLR_BG)], 
                  foreground=[('active', CLR_RED)])

        # LİSTE SEÇİM RENGİ FIX: CLR_RED
        style.configure("Treeview", background=CLR_CARD, fieldbackground=CLR_CARD, 
                        foreground=CLR_TEXT, rowheight=35, borderwidth=0)
        style.map("Treeview", background=[('selected', CLR_RED)], foreground=[('selected', 'white')])

    def create_layout(self):
        # --- HEADER ---
        header = tk.Frame(self.root, bg=CLR_BG)
        header.pack(fill='x', padx=40, pady=(30, 20))
        tk.Label(header, text="DEEPBYTE AUDITOR", bg=CLR_BG, fg=CLR_TEXT, font=('Impact', 26)).pack(side='left')
        
        # BUTON HOVER İPTAL
        self.btn_scan = tk.Button(header, text="PROJEYİ TARA", command=self.start_scan_thread,
                                 bg=CLR_RED, fg='white', activebackground=CLR_RED, 
                                 activeforeground='white', relief='flat', 
                                 font=('Segoe UI Bold', 10), padx=30, pady=10, bd=0)
        self.btn_scan.pack(side='right')

        # --- TABS ---
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill='both', expand=True, padx=40, pady=(0, 20))
        self.tab_dash = tk.Frame(self.tabs, bg=CLR_BG)
        self.tab_list = tk.Frame(self.tabs, bg=CLR_BG)
        self.tabs.add(self.tab_dash, text=" DASHBOARD ")
        self.tabs.add(self.tab_list, text=" DOSYA REHBERİ ")

        self.dash_content = tk.Frame(self.tab_dash, bg=CLR_BG)
        self.dash_content.pack(fill='both', expand=True, pady=10)
        self.setup_list_view()

        # --- SIGNATURE FOOTER (DİKEY & STATİK) ---
        footer = tk.Frame(self.root, bg=CLR_BG)
        footer.pack(fill='x', side='bottom', padx=40, pady=(0, 20))

        sig_frame = tk.Frame(footer, bg=CLR_BG)
        sig_frame.pack(side='right')

        # Üst Satır: Developed by gktrk363 (Kırmızı)
        tk.Label(sig_frame, text="Developed by gktrk363 <3", bg=CLR_BG, fg=CLR_RED, 
                 font=('Segoe UI Bold', 10)).pack(anchor='e')

        # Alt Satır: Source Code (Beyaz & Tıklanabilir)
        repo_url = "github.com/gktrk363/deepbyte-auditor"
        self.repo_lbl = tk.Label(sig_frame, text=f"Source Code: {repo_url}", bg=CLR_BG, fg=CLR_TEXT, 
                                 font=('Segoe UI Semibold', 8), cursor="hand2")
        self.repo_lbl.pack(anchor='e', pady=(2, 0))

        # Tıklama İşlevi Aktif
        self.repo_lbl.bind("<Button-1>", lambda e: webbrowser.open(f"https://{repo_url}"))

    def format_bytes(self, size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024: return f"{size:.2f} {unit}"
            size /= 1024

    def setup_list_view(self):
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_data)
        tk.Entry(self.tab_list, textvariable=self.search_var, bg=CLR_CARD, fg=CLR_TEXT, 
                 insertbackground='white', relief='flat', font=('Segoe UI', 11)).pack(fill='x', pady=15, ipady=8)

        self.tree = ttk.Treeview(self.tab_list, columns=("Name", "Size", "Type", "Path"), show="headings")
        cols = {"Name": "Dosya", "Size": "Boyut", "Type": "Tür", "Path": "Konum"}
        for k, v in cols.items():
            self.tree.heading(k, text=v)
            self.tree.column(k, width=120)
        self.tree.column("Path", width=500)
        self.tree.pack(fill='both', expand=True)
        
        self.menu = tk.Menu(self.root, tearoff=0, bg=CLR_CARD, fg=CLR_TEXT)
        self.menu.add_command(label="Klasörde Göster", command=self.reveal_in_explorer)
        self.tree.bind("<Button-3>", lambda e: self.menu.post(e.x_root, e.y_root) if self.tree.identify_row(e.y) else None)

    def start_scan_thread(self):
        path = filedialog.askdirectory()
        if not path: return
        self.btn_scan.config(text="TARANIYOR...", state='disabled')
        threading.Thread(target=self.run_analysis, args=(path,), daemon=True).start()

    def run_analysis(self, path):
        raw_data = []
        for root, dirs, files in os.walk(path):
            rel = os.path.relpath(root, path)
            folder_root = rel.split(os.sep)[0] if rel != "." else "Root"
            for f in files:
                fp = os.path.join(root, f)
                try:
                    s = os.path.getsize(fp)
                    ext = os.path.splitext(f)[1].lower()
                    stype = ext if ext else "Binary Data"
                    if ".git" in root: stype = "Git History"
                    raw_data.append({'Name': f, 'Size': s, 'Type': stype, 'Path': fp, 'Folder': folder_root})
                except: continue
        self.df = pd.DataFrame(raw_data)
        self.root.after(0, self.update_ui)

    def update_ui(self):
        self.render_charts()
        self.filter_data()
        self.btn_scan.config(text="PROJEYİ TARA", state='normal')

    def render_charts(self):
        for w in self.dash_content.winfo_children(): w.destroy()
        plt.style.use('dark_background')
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), facecolor=CLR_BG)
        plt.subplots_adjust(wspace=0.4, right=0.8)

        ext_data = self.df.groupby('Type')['Size'].sum().sort_values().tail(6)
        ax1.barh(ext_data.index, ext_data.values / (1024**2), color=CLR_RED)
        ax1.set_title("Uzantı Ağırlıkları (MB)", color=CLR_SUB, fontsize=9)
        ax1.tick_params(colors=CLR_SUB, labelsize=8)

        folder_data = self.df.groupby('Folder')['Size'].sum().sort_values(ascending=False)
        total_size = folder_data.sum()
        threshold = total_size * 0.04
        main_f = folder_data[folder_data >= threshold]
        if folder_data[folder_data < threshold].any(): main_f['Diğer'] = folder_data[folder_data < threshold].sum()

        wedges, texts = ax2.pie(main_f.values, startangle=90, colors=PALETTE[:len(main_f)],
                                 wedgeprops={'width': 0.4, 'edgecolor': CLR_BG})
        ax2.legend(wedges, main_f.index, title="Klasörler", loc="center left", 
                   bbox_to_anchor=(1, 0, 0.5, 1), fontsize=7, frameon=False)
        ax2.text(0, 0, f"{self.format_bytes(total_size)}\n{len(self.df):,} Dosya", ha='center', va='center', color='white', fontweight='bold', fontsize=9)
        ax2.set_title("Hiyerarşik Dağılım", color=CLR_SUB, fontsize=9)

        canvas = FigureCanvasTkAgg(fig, master=self.dash_content)
        canvas.draw(); canvas.get_tk_widget().pack(fill='both', expand=True)

    def filter_data(self, *args):
        query = self.search_var.get().lower()
        for i in self.tree.get_children(): self.tree.delete(i)
        if self.df.empty: return
        filtered = self.df[self.df['Name'].str.lower().str.contains(query, na=False)]
        for _, r in filtered.sort_values('Size', ascending=False).head(100).iterrows():
            self.tree.insert("", "end", values=(r['Name'], self.format_bytes(r['Size']), r['Type'], r['Path']))

    def reveal_in_explorer(self):
        sel = self.tree.selection()
        if sel: webbrowser.open(os.path.dirname(self.tree.item(sel[0], "values")[3]))

if __name__ == "__main__":
    try: from ctypes import windll; windll.shcore.SetProcessDpiAwareness(1)
    except: pass
    root = tk.Tk(); app = DeepByteAuditor(root); root.mainloop()