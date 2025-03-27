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
window.title("Relabel (LEI)")
window.geometry("300x147")

# Add buttons
btn1 = tk.Button(window, text="Angiovue", command=run_angiovue, width=25)
btn1.pack(pady=10)

btn2 = tk.Button(window, text="Revo", command=run_revo, width=25)
btn2.pack(pady=10)

btn3 = tk.Button(window, text="Spectralis", command=run_spectralis, width=25)
btn3.pack(pady=10)

# Start the main event loop
window.mainloop()
