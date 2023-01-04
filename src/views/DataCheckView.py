import re
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np

from models.GestureEnum import Gesture


class DataCheckView(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.pack(fill=tk.BOTH, expand=True)

        # Frame
        self.frame = ttk.Label(self)
        self.frame.pack(fill=tk.X, expand=True)

        self.under_bar = ttk.Frame(self)
        self.under_bar.pack(fill=tk.X, side = tk.BOTTOM, expand=True)

        self.message_label = ttk.Button(self.under_bar, text='Save Capture', command=self.save_image)
        self.message_label.grid(row=0, column=1)

        self.reset_dataset = ttk.Button(self.under_bar, text='Reset', command=self.save_image)
        self.reset_dataset.grid(row=0, column=2)

        self.view_history = ttk.Button(self.under_bar, text='History', command=self.save_image)
        self.view_history.grid(row=0, column=0)



        # Gestures        
        self.opcion = tk.IntVar() 
        self.gesture_panel = ttk.Frame(self)
        self.gesture_panel.pack(side=tk.BOTTOM)
        self.gesture_rbs = []
        self.gesture_labels = []

        self.gesture_scroll = tk.Scrollbar(self.gesture_panel, orient='horizontal')
        self.gesture_scroll.pack(side=tk.BOTTOM, fill='x')

        for index, gesture in enumerate(Gesture):
            actions_frame = ttk.Frame(self.gesture_scroll)
            rb = tk.Radiobutton(
                actions_frame, 
                text=gesture.name,
                variable=self.opcion, 
                value=index,
                command=self.change_gesture,
                indicator=0,
                background = "light blue")

            gesture_label = ttk.Label(actions_frame, text=f"{0}")

            #actions_frame.grid(row=0)
            
            self.gesture_rbs += [rb]
            self.gesture_labels += [gesture_label]

            rb.grid(row=0, column=0)
            gesture_label.grid(row=1, column=0)
            
            actions_frame.grid(row=0, column=index, sticky='ew',ipady = 5, ipadx=5)
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

    def refresh_count(self, count_list):
        for i, _ in enumerate(self.gesture_labels):
            self.gesture_labels[i].config(text = count_list[i])

    def change_gesture(self):
        self.controller.change_gesture()

    def save_image(self):
        self.controller.save_image()