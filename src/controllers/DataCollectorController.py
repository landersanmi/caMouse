import cv2
from PIL import Image
from PIL import ImageTk
from datetime import datetime
import time
import numpy as np
from tkinter import filedialog
import pandas as pd
import random
import pickle



import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

class DataCollectorController:
    
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.visualization_frame = self.view.visualization_frame
        self.load_gesture_names_combo()
        self.knn_model = pickle.load(open(self.model.test_model_dir, 'rb'))
        matplotlib.use("Agg")
 
    def update_frames(self):
        frames = []
        for i, cam in enumerate(self.model.cameras):
            _, frame = cam.read()
            if frame.shape[1] > 720:
                frame = cv2.resize(frame, (int(frame.shape[1]*0.5), int(frame.shape[0]*0.5)), interpolation = cv2.INTER_AREA)
            
            frame = cv2.flip(frame, 1)
            frame, landmarks_normalized, landmarks_raw = self.get_drawed_hand_frame(frame, self.model.hands[i])

            model_data = []
            x, y, z = [], [], []
            for lm in landmarks_normalized:
                x.append(lm[0])
                y.append(lm[1])
                z.append(lm[2])
                model_data.append(lm[0])
                model_data.append(lm[1])
                model_data.append(lm[2])

            if len(model_data) > 0 and self.view.config_frame.test_mode_var.get() == 1:
                model_data = np.asarray(model_data).reshape(1, -1)
                predict_df = pd.DataFrame(data = model_data, columns=self.model.columnames[:-1])
                predicted_gesture = self.knn_model.predict(predict_df)[0]
                cv2.putText(frame, str(predicted_gesture), (0,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255))
            frames.append(frame)
            if self.visualization_frame.camera_frames is not None and len(self.visualization_frame.camera_frames) >= i+1:
                self.set_camera_label_image(frame, self.visualization_frame.camera_frames[i].cam_lbl)
            
            if len(landmarks_normalized) != 0: 
                plot = self.generate_3D_plot(x, y, z)
                self.set_hand_label_image(plot, self.visualization_frame.camera_frames[i].hand_lbl)
                gesture = self.view.config_frame.gesture_var.get()

                if self.model.is_recording and random.random()< 0.4: 
                    self.model.add_gesture_series(landmarks_raw, gesture)
        
        self.model.frames = frames

    def generate_3D_plot(self, x, y, z):
        plt.close('all')
        fig = plt.figure(figsize=(4, 3), dpi=50)
        canvas = FigureCanvasAgg(fig)
        ax = plt.axes(projection='3d')
        ax.scatter3D(x, y, z)
        canvas.draw()
        buf = canvas.buffer_rgba()
        plot = np.asarray(buf)
        return plot

    def set_hand_label_image(self, image, lbl):
        tk_hand_mage = ImageTk.PhotoImage(Image.fromarray(image))
        self.set_label_image(lbl, tk_hand_mage)

    def set_camera_label_image(self, image, lbl):
        tk_camera_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))
        self.set_label_image(lbl, tk_camera_image)
    
    def set_label_image(self, lbl, image):
        lbl.configure(image=image)
        lbl.image = image
    
    def get_drawed_hand_frame(self, frame, hand):
        x , y, c = frame.shape
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hand.process(framergb)

        landmarks_raw = []
        landmarks_coordinates = np.empty((0,3), int)
        landmarks_coordinates_normalized = np.empty((0,3), int)
        if result.multi_hand_landmarks:
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    lmx, lmy, lmz = int(lm.x * x), int(lm.y * y), int(lm.z * c)
                    landmarks_coordinates = np.append(landmarks_coordinates, [[lmx, lmy, lmz]] , axis=0)
                    landmarks_raw.append([lm.x, lm.y, lm.z])
                
                landmarks_coordinates_normalized = landmarks_coordinates - landmarks_coordinates.min(axis=0)
                self.model.mpDraw.draw_landmarks(frame, handslms, self.model.mpHands.HAND_CONNECTIONS)
        
        return frame, landmarks_coordinates_normalized, landmarks_raw


    def add_cam(self):
        try:
            camera_id = int(self.view.config_frame.cam_id_var.get())
        except:
            camera_id = str(self.view.config_frame.cam_id_var.get())

        camera = cv2.VideoCapture(camera_id)
        if camera != None:
            s = self.model.cameras.append(camera)
            self.model.update_hands()
            return True
        return False
    
    def add_cam_frame(self):
        self.view.add_cam_frame()

    def get_cam_count(self):
        return len(self.model.cameras)

    def load_gesture_names_combo(self):
        self.view.set_gestures(self.model.gesture_types)

    def select_dir(self):
        folder_selected = filedialog.askdirectory()
        self.view.config_frame.dir_var.set(folder_selected)

    def select_model(self):
        file_selected = filedialog.askopenfilename(title="Select model file...", filetypes=[('pickle files', '.pkl')])
        self.model.test_model_dir = file_selected
        self.knn_model = pickle.load(open(file_selected, 'rb'))
        self.view.config_frame.model_dir_var.set(file_selected)

    def update_secs(self):
        self.model.record_time = int(self.config_frame.secs_var)


    def record_data(self):
        self.model.is_recording = True
        time.sleep(int(self.view.config_frame.secs_var.get()))
        self.model.is_recording = False
        print(self.model.gestures_df)

    def save_data(self):
        path = self.view.config_frame.dir_var.get() + '/'
        filename = str(datetime.timestamp(datetime.now())) + '.csv'
        self.model.gestures_df.to_csv(path + filename)