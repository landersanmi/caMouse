from tkinter import ttk
import tkinter as tk
import threading
import numpy as np
import math

class DataCollectorView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.controller = None

        self.upper_frame = ttk.Frame(parent)
        self.config_frame = ConfigFrame(self.upper_frame, self.controller)
        self.config_frame.pack(side=tk.LEFT)
        self.visualization_frame = VisualizationFrame(self.upper_frame, self.controller)
        self.visualization_frame.pack(side=tk.RIGHT)
        self.upper_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH, pady=10)

        self.bottom_frame = ttk.Frame(parent)
        self.btns_frame = ttk.Frame(self.bottom_frame)
        ttk.Button(self.btns_frame, text="Record Data", style="Accent.TButton", command=self.on_record_btn).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(self.btns_frame, text="Save Data", style="Accent.TButton", command= self.on_save_btn).pack(side=tk.LEFT, padx=10, pady=10)
        self.btns_frame.pack(side=tk.LEFT)
        self.bottom_frame.pack(side=tk.BOTTOM)

    def set_controller(self, controller):
        self.controller = controller
        self.visualization_frame.controller = controller
        self.config_frame.controller = controller

    def update_cameras_loop(self):
        while(True):
            if self.controller:
                self.controller.update_frames()

    def set_gestures(self, gesture_types):
        self.config_frame.gesture_combo['values'] = gesture_types

    def add_cam_frame(self):
        new_camera = CameraFrame(self.visualization_frame.cameras_frame, controller=self.controller)
        self.visualization_frame.camera_frames = np.append(self.visualization_frame.camera_frames, new_camera)
        new_camera.pack(side=tk.TOP)#, fill=tk.BOTH, expand=False)
    
    def on_record_btn(self):
        if self.controller:
            record_thread = threading.Thread(target=self.controller.record_data)
            record_thread.start()

    def on_save_btn(self):
        if self.controller:
            self.controller.save_data()


class ConfigFrame(ttk.Frame):
    def __init__(self, window, controller):
        super().__init__(window)   

        # NEW CAMERA
        self.config_cam_id_frame = ttk.LabelFrame(self, text="New camera options")
        self.cam_id_var = tk.StringVar()
        ttk.Label(self.config_cam_id_frame, text="Camera ID:").pack(side=tk.LEFT, padx=10)
        ttk.Entry(self.config_cam_id_frame, textvariable=self.cam_id_var).pack(side=tk.LEFT, pady=10)
        ttk.Button(self.config_cam_id_frame, text="Add camera", command=self.on_add_cam_btn).pack(side=tk.RIGHT, padx=10)
        self.config_cam_id_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

        # GESTURE
        self.config_gesture_frame = ttk.LabelFrame(self, text="Gesture selection")
        self.gesture_var = tk.StringVar()
        self.gesture_var.set("None")
        ttk.Label(self.config_gesture_frame, text="Gesture:").pack(side=tk.LEFT, padx=10)
        self.gesture_combo = ttk.Combobox(self.config_gesture_frame, values=['None'], textvariable=self.gesture_var)
        self.gesture_combo.pack(side=tk.LEFT, pady=10)
        self.config_gesture_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)
        
        # RECORDING TIME
        self.config_secs_frame = ttk.LabelFrame(self, text="Recording time")
        self.secs_var = tk.StringVar()
        ttk.Label(self.config_secs_frame, text="Seconds:").pack(side=tk.LEFT, padx=10)
        ttk.Entry(self.config_secs_frame, textvariable=self.secs_var).pack(side=tk.LEFT, pady=10)
        self.config_secs_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

        # SAVE DIR
        self.config_dir_frame = ttk.LabelFrame(self, text="Data saving directory")
        self.dir_lbl = ttk.Label(self.config_dir_frame, text="Directory:").pack(side=tk.LEFT, padx=10)
        self.dir_var = tk.StringVar()
        ttk.Entry(self.config_dir_frame, textvariable=self.dir_var).pack(side=tk.LEFT, pady=10)
        ttk.Button(self.config_dir_frame, text="Open directory selector", command=self.on_select_dir_btn).pack(side=tk.RIGHT, padx=10)
        self.config_dir_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

        # TEST MODEL
        self.config_test_mode_frame = ttk.LabelFrame(self, text="Testing model options")
        
        self.model_dir_frame = ttk.Frame(self.config_test_mode_frame)
        ttk.Label(self.model_dir_frame, text="Model file:").pack(side=tk.LEFT, padx=10)
        self.model_dir_var = tk.StringVar()
        ttk.Entry(self.model_dir_frame, textvariable=self.model_dir_var).pack(side=tk.LEFT, pady=10)
        ttk.Button(self.model_dir_frame, text="Open file selector", command=self.on_select_model_btn).pack(side=tk.RIGHT, padx=10)
        self.model_dir_frame.pack(side=tk.TOP, fill=tk.X)

        self.test_mode_frame = ttk.Frame(self.config_test_mode_frame)
        self.test_mode_var = tk.IntVar(value=2)
        ttk.Label(self.test_mode_frame, text="Test mode:").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(self.test_mode_frame, text="Yes", variable=self.test_mode_var, value=1).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(self.test_mode_frame, text="No", variable=self.test_mode_var, value=2).pack(side=tk.LEFT, padx=10)
        self.test_mode_frame.pack(side=tk.TOP, fill=tk.X)

        self.config_test_mode_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

        self.controller = controller
    
    def on_add_cam_btn(self):
        if self.controller:
            if self.controller.add_cam():
                self.controller.add_cam_frame()
    
    def on_select_dir_btn(self):
        if self.controller:
            self.controller.select_dir()
    
    def on_select_model_btn(self):
        if self.controller:
            self.controller.select_model()

    def on_secs_txt_change(self):
        if self.controller:
            self.controller.update_secs()


class VisualizationFrame(ttk.Frame):
    def __init__(self, window, controller):
        super().__init__(window)   
        
        '''
        self.cameras_container = ttk.Frame(window)
        self.canvas = tk.Canvas(self.cameras_container)
        self.scrollbar = ttk.Scrollbar(self.cameras_container, orient=tk.VERTICAL, command=self.canvas.yview)
        self.cameras_frame = ttk.Frame(self.canvas)
        self.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox(tk.ALL)
            )
        )
        self.canvas.create_window((0, 0), window=self.cameras_frame, anchor=tk.NW)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.cameras_container.pack(side=tk.TOP)
        '''
        self.cameras_frame = ttk.Frame(window)
        self.cameras_frame.pack(side=tk.TOP)#, fill=tk.Y, expand=True)

        self.camera_frames = []
        self.controller = controller


class CameraFrame(ttk.Frame):
    def __init__(self, window, controller):
        super().__init__(window,)

        self.cam_lbl = ttk.Label(window)
        self.hand_lbl = ttk.Label(window)
        cam_count = controller.get_cam_count()
        #if cam_count % 3 == 0:
            #column = 4
        if cam_count % 2 == 0:
            column = 2
        else:
            column = 0
        row = math.floor((cam_count-0.00000001)/2)

        self.cam_lbl.grid(row=row, column=column)#pack(side=tk.LEFT)
        self.hand_lbl.grid(row=row, column=column+1)#pack(side=tk.LEFT) 


