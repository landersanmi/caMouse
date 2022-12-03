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

class DataCollectorController:
    
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.visualization_frame = self.view.visualization_frame
        self.load_gesture_names_combo()
        self.knn_model = pickle.load(open('../models/knn.pkl', 'rb'))
 
    def update_frames(self):
        frames = []
        for i, cam in enumerate(self.model.cameras):
            _, frame = cam.read()
            if frame.shape[1] > 720:
                frame = cv2.resize(frame, (int(frame.shape[1]*0.5), int(frame.shape[0]*0.5)), interpolation = cv2.INTER_AREA)
            
            frame = cv2.flip(frame, 1)
            frame, landmarks_coordinates, landmarks_raw = self.get_drawed_hand_frame(frame, self.model.hands[i])
            rect = cv2.boundingRect(landmarks_coordinates)
            _, _, w, h = rect
            black_frame = np.zeros((h,w), dtype=int)
            data=[]
            for landmarks in landmarks_raw: 
                data.append(landmarks[0])
                data.append(landmarks[1])
                data.append(landmarks[2])

            for coordinates in landmarks_coordinates:
                cv2.circle(black_frame, (coordinates[0], coordinates[1]), 2, (255,0,0), -1)

            
            if len(data) > 0:
                predicted_gesture = self.knn_model.predict(np.asarray(data).reshape(1, -1))[0]
                cv2.putText(frame, str(predicted_gesture), (0,40), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,255))
            frames.append(frame)
            if self.visualization_frame.camera_frames is not None and len(self.visualization_frame.camera_frames) >= i+1:
                self.set_camera_label_image(frame, self.visualization_frame.camera_frames[i].cam_lbl)
            
            if len(landmarks_coordinates) != 0: 
                self.set_hand_label_image(black_frame, self.visualization_frame.camera_frames[i].hand_lbl)
                gesture = self.view.config_frame.gesture_var.get()

                if self.model.is_recording and random.random()< 0.05: 
                    self.model.add_gesture_series(landmarks_raw, gesture)
        
        self.model.frames = frames

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
        landmarks_coordinates = np.empty((0,2), int)
        landmarks_coordinates_normalized = np.empty((0,2), int)
        if result.multi_hand_landmarks:
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    lmx, lmy, lmz = int(lm.x * x), int(lm.y * y), int(lm.z * c)
                    cv2.circle(frame, (lmx, lmy), 3, (255,0,0), -1)
                    landmarks_coordinates = np.append(landmarks_coordinates, [[lmx, lmy]] , axis=0)
                    landmarks_raw.append([lm.x, lm.y, lm.z])
                
                landmarks_coordinates_normalized = landmarks_coordinates - landmarks_coordinates.min(axis=0)
                #for dot in dots_relocated: cv2.circle(frame, (dot[0], dot[1]), 3, (0,0,255), -1)
                rect = cv2.boundingRect(landmarks_coordinates)
                x, y, w, h = rect
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
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