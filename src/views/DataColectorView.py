from tkinter import ttk
import tkinter as tk
import threading
import numpy as np

class DataColectorView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)


        self.config_frame = ttk.Frame(parent)
        #self.config_frame.pack(side="left")
        self.config_frame.grid(row=0, column=0, padx=0, pady=0)

        # NEW CAMERA
        self.cam_lbl = ttk.Label(self.config_frame, text="New camera options").pack(side="top")
        self.config_cam_id_frame = ttk.Frame(self.config_frame)
        self.cam_id_var = tk.StringVar()
        self.cam_id_lbl = ttk.Label(self.config_cam_id_frame, text="ID:").pack(side="left")
        self.cam_id_txt = ttk.Entry(self.config_cam_id_frame, textvariable=self.cam_id_var).pack(side="left")
        self.config_cam_id_frame.pack(side="top")
        self.add_cam_btn = ttk.Button(self.config_frame, text="Add camera", command=self.on_add_cam_btn).pack(side="top")

        # GESTURE
        self.gesture_lbl = ttk.Label(self.config_frame, text="Select a gesture").pack(side="top")
        self.gesture_var = tk.StringVar()
        self.gesture_var.set("None")
        self.gesture_combo = ttk.Combobox(self.config_frame, values=['None'], textvariable=self.gesture_var)
        self.gesture_combo.pack(side="top")
        
        # RECORDING TIME
        self.record_time_lbl = ttk.Label(self.config_frame, text="Recordindg Time").pack(side="top")
        self.config_secs_frame = ttk.Frame(self.config_frame)
        self.secs_var = tk.StringVar()
        self.secs_lbl = ttk.Label(self.config_secs_frame, text="Seconds:").pack(side="left")
        self.secs_txt = ttk.Entry(self.config_secs_frame, textvariable=self.secs_var).pack(side="left")
        self.config_secs_frame.pack(side="top")

        # SAVE DIR
        self.save_dir_lbl = ttk.Label(self.config_frame, text="Save directory").pack(side="top")
        self.config_dir_frame = ttk.Frame(self.config_frame)
        self.dir_lbl = ttk.Label(self.config_dir_frame, text="Directory:").pack(side="left")
        self.dir_var = tk.StringVar()
        self.dir_txt = ttk.Entry(self.config_dir_frame, textvariable=self.dir_var).pack(side="left")
        self.config_dir_frame.pack(side="top")
        self.zelect_dir_btn = ttk.Button(self.config_frame, text="Select Directory", command=self.on_select_dir_btn).pack(side="top")

        # CAMERAS PANEL
        self.display_frame = ttk.Frame(parent)

        self.btns_frame = ttk.Frame(self.display_frame)
        self.record_btn = ttk.Button(self.btns_frame, text="Record Data", command=self.on_record_btn).grid(row=0, column=0)#.pack(side="left")
        self.save_data_btn = ttk.Button(self.btns_frame, text="Save Data", command= self.on_save_btn).grid(row=0, column=1)#.pack(side="left")
        self.btns_frame.grid(row = 0, column = 0)

        self.cameras_frame = ttk.Frame(self.display_frame)
        
        self.scroll_frame = ttk.Frame(self.cameras_frame)
        self.scrollbar= ttk.Scrollbar(self.scroll_frame, orient="vertical")
        self.scrollbar.grid(row=0, column=0)
        self.scroll_frame.grid(row=0, column=1)
        
        self.cameras_frame.grid(row=1, column=0)

        self.cam_lbls = []
        self.hand_lbls = []

        #self.display_frame.pack(side ="left")
        self.display_frame.grid(row=0, column=1)
        
        self.controller = None

    def set_controller(self, controller):
        self.controller = controller


    def on_add_cam_btn(self):
        if self.controller:
            if self.controller.add_cam():
                self.add_cam_frame()
    
    def add_cam_frame(self):

        cam_count = self.controller.get_cam_count()
        self.cams_frame = ttk.Frame(self.cameras_frame)
        self.cam_frame = ttk.Frame(self.cams_frame)
        self.cam_lbl = tk.Label(self.cam_frame)
        self.cam_lbl.grid(row=0, column=0)#pack(side="left")  
        self.hand_lbl = tk.Label(self.cam_frame, width=200)
        self.hand_lbl.grid(row=0, column=1)#pack(side="left")
        #self.cam_frame.pack(side="top")
        self.cam_lbls = np.append(self.cam_lbls, self.cam_lbl)
        self.hand_lbls = np.append(self.hand_lbls, self.hand_lbl)
        self.cam_frame.grid(row=cam_count-1,column=0)
        self.cams_frame.grid(row=0, column=0)

    def on_select_dir_btn(self):
        if self.controller:
            self.controller.select_dir()

    def on_record_btn(self):
        if self.controller:
            record_thread = threading.Thread(target=self.controller.record_data)
            record_thread.start()

    def on_save_btn(self):
        if self.controller:
            self.controller.save_data()

    def on_secs_txt_change(self):
        if self.controller:
            self.controller.update_secs()

    def update_cameras_loop(self):
        while(True):
            if self.controller:
                self.controller.update_frames()

    def set_gestures(self, gesture_types):
        self.gesture_combo['values'] = gesture_types

