import re
import tkinter as tk
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg
from tkinter import ttk
from PIL import Image, ImageTk

from models.GestureEnum import Gesture

HAND_CONNECTIONS = [(0, 1), (0, 5), (0, 17), (1, 2), (2, 3), (3, 4), (5, 6), (5, 9), 
                    (6, 7), (7, 8), (9, 10), (9, 13), (10, 11), (11, 12), (13, 14), 
                    (13, 17), (14, 15), (15, 16), (17, 18), (18, 19), (19, 20)]


class HistoryWindow(tk.Toplevel):

    def __init__(self, main):
        super().__init__()
        
        self.history_data = pd.read_csv('data/history.csv')
        self.current_id = self.history_data.shape[0]-1
        self.current_predicted_gesture = self.history_data.iloc[-1][0]
        self.plot = None
        self.load_window()
        self.plot_current_id_hand()
    
    def plot_current_id_hand(self):
        row = self.history_data.iloc[self.current_id]
        category = row[0]
        data = row[1:64]
        plot = self.generate_3D_plot(data, category)
        tk_hand_image = ImageTk.PhotoImage(Image.fromarray(plot))
        if self.plot != None:
            self.plot.configure(image=tk_hand_image)
            self.plot.image = tk_hand_image

    def load_window(self):
        
        self.main = ttk.Frame(self)
        self.main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.slider_value = tk.IntVar()
        self.slider = ttk.Scale(self.main, from_=0, to=self.current_id, orient='horizontal', variable=self.slider_value, command=self.on_slider_change)
        self.slider.set(self.current_id)
        self.slider.pack(side=tk.TOP, fill=tk.X, expand=True, padx=10)

        self.predicted_gesture_label = ttk.Label(self.main, text="Predicted gesture ID: " + str(self.current_predicted_gesture))
        self.predicted_gesture_label.pack(side=tk.TOP)

        self.plot = ttk.Label(self.main)
        self.plot.pack(side=tk.TOP, fill=tk.X, expand=True)
        

    def on_slider_change(self, event):
        self.current_id = self.slider_value.get()
        self.plot_current_id_hand()
        self.current_predicted_gesture = self.history_data.iloc[self.current_id][0]
        try:
            self.predicted_gesture_label.config(text="Predicted gesture ID: " + str(self.current_predicted_gesture))
        except:
            pass
    def generate_3D_plot(self, data, category):
        plt.close('all')
        fig = plt.figure(figsize=(8, 8), dpi=75)
        canvas = FigureCanvasAgg(fig)
        ax = plt.axes(projection='3d')
        
        x, y, z = [], [], []
        for i in range(0, len(data)-2, 3):
            x = np.append(x, data[i])
            y = np.append(y, data[i+1])
            z = np.append(z, data[i+2])

        ax.scatter3D(x, y, z, s=6)

        for connection in HAND_CONNECTIONS:
            x1, x2 = x[connection[0]], x[connection[1]]
            y1, y2 = y[connection[0]], y[connection[1]]
            z1, z2 = z[connection[0]], z[connection[1]]
            X, Y, Z = [x1, x2], [y1, y2], [z1, z2]
            ax.plot(X, Y, zs=Z, linewidth=10, color='b')
        
        canvas.draw()
        buf = canvas.buffer_rgba()
        plot = np.asarray(buf)
        return plot