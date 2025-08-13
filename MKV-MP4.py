import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from threading import Thread

# Funktion til at konvertere MKV til MP4
def convert_mkv_to_mp4(input_files):
    if not input_files:
        messagebox.showerror("Fejl", "Vælg mindst én gyldig MKV-fil")
        return

    def run_conversion():
        total_files = len(input_files)
        for index, input_file in enumerate(input_files):
            if not input_file.lower().endswith(".mkv"):
                continue

            output_file = input_file.rsplit(".", 1)[0] + ".mp4"
            try:
                command = ["ffmpeg", "-i", input_file, "-c:v", "copy", "-c:a", "copy", output_file]
                subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            except Exception as e:
                messagebox.showerror("Fejl", f"Fejl ved konvertering af {input_file}: {e}")
            
            progress_var.set((index + 1) / total_files * 100)
            root.update_idletasks()
        
        messagebox.showinfo("Succes", "Konvertering færdig!")

    Thread(target=run_conversion).start()

# Funktion til at vælge flere filer
def select_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("MKV filer", "*.mkv")])
    if file_paths:
        entry_var.set("; ".join(file_paths))
        selected_files.clear()
        selected_files.extend(file_paths)

# Opret GUI
root = tk.Tk()
root.title("MKV til MP4 Konverter")
root.geometry("500x250")
root.resizable(False, False)

entry_var = tk.StringVar()
selected_files = []

tk.Label(root, text="Vælg MKV-filer:").pack(pady=10)
entry = tk.Entry(root, textvariable=entry_var, width=60, state='readonly')
entry.pack()

tk.Button(root, text="Gennemse", command=select_files).pack(pady=5)
tk.Button(root, text="Konverter", command=lambda: convert_mkv_to_mp4(selected_files)).pack(pady=10)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=400)
progress_bar.pack(pady=10)

root.mainloop()
