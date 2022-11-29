from tkinter import ttk
import tkinter as tk
import threading

class DataColectorView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.config_frame = ttk.Frame(self)
        self.config_frame.pack(side="left")

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
        self.gesture_var.set("Mouse Move")
        self.gesture_combo = ttk.Combobox(self.config_frame, values=["Mouse Move", "Left Click", "Right Click", "Zoom"], textvariable=self.gesture_var).pack(side="top")
        
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


        self.display_frame = ttk.Frame(self)

        self.btns_frame = ttk.Frame(self.display_frame)
        self.record_btn = ttk.Button(self.btns_frame, text="Record Data", command=self.on_record_btn).pack(side="left")
        self.save_data_btn = ttk.Button(self.btns_frame, text="Save Data", command= self.on_save_btn).pack(side="left")
        self.btns_frame.pack(side="top", pady=10)

        self.cam0_frame = ttk.Frame(self.display_frame)
        self.cam0_lbl = tk.Label(self.cam0_frame)
        self.cam0_lbl.pack(side="left")  
        self.hand0_lbl = tk.Label(self.cam0_frame)
        self.hand0_lbl.pack(side="left")   
        self.cam0_frame.pack(side="top")

        self.cam1_frame = ttk.Frame(self.display_frame)
        self.cam1_lbl = tk.Label(self.cam0_frame)
        self.cam1_lbl.pack(side="left")  
        self.hand1_lbl = tk.Label(self.cam0_frame)
        self.hand1_lbl.pack(side="left")   
        self.cam1_frame.pack(side="top")

        self.cam2_frame = ttk.Frame(self.display_frame)
        self.cam2_lbl = tk.Label(self.cam0_frame)
        self.cam2_lbl.pack(side="left")  
        self.hand2_lbl = tk.Label(self.cam0_frame)
        self.hand2_lbl.pack(side="left")   
        self.cam2_frame.pack(side="top")

        self.display_frame.pack(side ="left")

        self.controller = None


    def set_controller(self, controller):
        self.controller = controller


    def on_add_cam_btn(self):
        if self.controller:
            self.controller.add_cam()

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


