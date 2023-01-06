import re
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np

from models.GestureEnum import Gesture
from .HistoryView import HistoryWindow

class DataCheckView(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.pack(fill=tk.BOTH, expand=True)

        self.left_col = ttk.Frame(self)
        self.left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.right_col = tk.Frame(self, bg="black")
        self.right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        
        

        # Frame
        self.frame = ttk.Label(self.left_col)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Button Bar
        self.under_bar = ttk.Frame(self.left_col)
        self.under_bar.pack(fill=tk.X, side = tk.BOTTOM, expand=True)


        self.message_label = ttk.Button(self.under_bar, text='Capture', command=self.save_image)
        self.message_label.grid(row=0, column=2)

        self.reset_dataset = ttk.Button(self.under_bar, text='Play', command=self.toggle_mouse_control)
        self.reset_dataset.grid(row=0, column=1)
        
        self.reset_dataset = ttk.Button(self.under_bar, text='Reset', command=self.reset_data)
        self.reset_dataset.grid(row=0, column=3)

        self.view_history = ttk.Button(self.under_bar, text='History', command=self.get_history)
        self.view_history.grid(row=0, column=0)



        # Gestures        
        self.opcion = tk.IntVar() 
        self.gesture_panel = tk.Frame(self.right_col, bg="red")
        
        self.gesture_panel.grid_columnconfigure(0, weight=1)
        self.gesture_panel.grid_rowconfigure(0, weight=1)
        self.gesture_panel.grid_columnconfigure(1, weight=1)
        self.gesture_panel.grid_rowconfigure(1, weight=1)
        self.gesture_panel.grid_columnconfigure(2, weight=1)
        self.gesture_panel.grid_rowconfigure(2, weight=1)
        self.gesture_panel.grid_columnconfigure(3, weight=1)
        self.gesture_panel.grid_rowconfigure(3, weight=1)
        self.gesture_panel.pack(fill = tk.BOTH, expand=True)
        
        self.gesture_rbs = []
        self.gesture_labels = []

        #self.gesture_scroll = tk.Scrollbar(self.gesture_panel, orient='horizontal')
        #self.gesture_scroll.pack(side=tk.BOTTOM, fill='x')

        for index, gesture in enumerate(Gesture):
            
            actions_frame = tk.Frame(self.gesture_panel, bg="blue")
            rb = tk.Radiobutton(
                actions_frame, 
                text=gesture.name,
                variable=self.opcion, 
                value=index,
                command=self.change_gesture,
                indicator=0,
                background = "light blue")

            gesture_label = ttk.Label(actions_frame, text=f"{0}")

            
            self.gesture_rbs += [rb]
            self.gesture_labels += [gesture_label]

            rb.pack(side=tk.LEFT, expand=True)
            gesture_label.pack(side=tk.LEFT, expand=True)
            
            actions_frame.grid(row=index//3, column=index%3, sticky='NWSE')

        
        # message
        self.info_panel = ttk.Frame(self)
        self.distance = ttk.Label(self.info_panel, text='Min Distance: ')
        self.distance.pack()

        self.category = ttk.Label(self.info_panel, text='Category: ')
        self.category.pack()

        self.info_panel.pack(side=tk.BOTTOM, fill=tk.BOTH)

        
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
        
    def toggle_mouse_control(self):
        self.controller.toggle_mouse_controller()
        
    def reset_data(self):
        raise NotImplementedError("Not implemented.")
        
    def get_history(self):
        HistoryWindow(self)