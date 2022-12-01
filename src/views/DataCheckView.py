import re
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np

from models.DataColectorModel import GESTURES


class DataCheckView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.pack(fill=tk.BOTH, expand=True)

        # Frame
        self.frame = ttk.Label(self)
        self.frame.pack(fill=tk.X, expand=True)

        self.message_label = ttk.Button(self, text='Save Capture', command=self.save_image)
        self.message_label.pack(fill=tk.X, side = tk.BOTTOM, expand=True)

        # Gestures        
        self.opcion = tk.IntVar() 
        self.gesture_panel = ttk.Frame(self)
        self.gesture_panel.pack(side=tk.BOTTOM)
        self.gesture_rbs = []

        self.gesture_scroll = tk.Scrollbar(self.gesture_panel, orient='horizontal')
        self.gesture_scroll.pack(side=tk.BOTTOM, fill='x')

        for index, gesture in enumerate(GESTURES):
            rb = tk.Radiobutton(
                self.gesture_scroll, 
                text=gesture,
                variable=self.opcion, 
                value=index,
                command=self.change_gesture,
                indicator=0,
                background = "light blue")
            
            self.gesture_rbs += [rb]

            rb.grid(row=0, column=index, sticky='ew',ipady = 5, ipadx=5)
            #rb.pack()

        # message
        self.info_panel = ttk.Frame(self)
        self.distance = ttk.Label(self.info_panel, text='Min Distance: ')
        self.distance.pack()

        self.category = ttk.Label(self.info_panel, text='Category: ')
        self.category.pack()

        self.info_panel.pack(side=tk.BOTTOM, fill='x')

        
        

        # set the controller
        self.controller = None

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller


    def change_gesture(self):
        self.controller.change_gesture()

    def save_image(self):
        self.controller.save_image()