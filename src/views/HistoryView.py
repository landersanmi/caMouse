import re
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np

from models.GestureEnum import Gesture


class HistoryWindow(tk.Toplevel):

    def __init__(self, main):
        super().__init__()
        self.load_window()
        
        self.current_id = 0


    def load_window(self):
        
        
        self.main = ttk.Frame(self)
        self.main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.frame = ttk.Label(self.main)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        
        self.under_bar = ttk.Frame(self.main)
        self.under_bar.pack(fill=tk.X, side = tk.BOTTOM, expand=True)
        
        

        self.previous_image = ttk.Button(self.under_bar, text='Previous', command=self.load_previous)
        self.previous_image.grid(row=0, column=0)

        self.next_image = ttk.Button(self.under_bar, text='Next', command=self.load_next)
        self.next_image.grid(row=0, column=1)
        
    def load_previous(self):
        self.current_id -= 1
        
    def load_next(self):
        self.current_id += 1