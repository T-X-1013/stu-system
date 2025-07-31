import tkinter as tk
from tkinter import ttk
import pandas as pd

def main():
    root = tk.Tk()
    root.title("Sample tkinter App")

    label = ttk.Label(root, text="Hello, tkinter!")
    label.pack(padx=20, pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()