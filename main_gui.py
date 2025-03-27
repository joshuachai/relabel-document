import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# Suppress macOS Tkinter deprecation warning
os.environ['TK_SILENCE_DEPRECATION'] = '1'

# Define button action functions
def run_angiovue():
    try:
        subprocess.run(["python", "angiovue.py"], check=True)
        messagebox.showinfo("Success", "Successfully ran angiovue.py!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to run angiovue.py.")

def run_revo():
    try:
        subprocess.run(["python3", "relabel.py", "revo"], check=True)
        messagebox.showinfo("Success", "Successfully ran relabel.py revo!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to run relabel.py revo.")

def run_spectralis():
    try:
        subprocess.run(["python3", "relabel.py", "spectralis"], check=True)
        messagebox.showinfo("Success", "Successfully ran relabel.py spectralis!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to run relabel.py spectralis.")

# Create main window
window = tk.Tk()
window.title("OCTA Relabel Utility (LEI)")
window.geometry("400x240")
window.resizable(False, False)
window.configure(bg="#f5f5f5")  # Light background

# Title label
title = tk.Label(window, text="OCTA Relabel Tool", font=("Helvetica", 18, "bold"), bg="#f5f5f5", fg="#333")
title.pack(pady=15)

# Button styling
button_style = {
    "font": ("Helvetica", 12, "bold"),
    "bg": "#4CAF50",
    "fg": "black",
    "activebackground": "#45a049",
    "width": 25,
    "height": 2,
    "bd": 0,
    "relief": "flat"
}

# Add buttons
btn1 = tk.Button(window, text="Run Angiovue", command=run_angiovue, **button_style)
btn1.pack(pady=5)

btn2 = tk.Button(window, text="Run Revo", command=run_revo, **button_style)
btn2.pack(pady=5)

btn3 = tk.Button(window, text="Run Spectralis", command=run_spectralis, **button_style)
btn3.pack(pady=5)

# Start the main event loop
window.mainloop()
