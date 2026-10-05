# main.py
import tkinter as tk
from tkinter import ttk
from ui import HospitalAppUI

if __name__ == '__main__':
    root = tk.Tk()
    root.title("🏥 Smart Hospital - Department Queue Scheduling System")
    root.geometry("1200x800")
    
    style = ttk.Style()
    if "clam" in style.theme_names(): 
        style.theme_use("clam")
        
    app = HospitalAppUI(root)
    
    root.mainloop()