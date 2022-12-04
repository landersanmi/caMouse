import cv2
import pandas as pd
import mediapipe as mp
import os

NUM_HAND_LANDMARKS = 21
GESTURES = ['RightIndexExtended', 'RightIndexHook', 'RightIndexClosed',
            'LeftIndexExtended', 'LeftIndexHook', 'LeftIndexClosed', 
            'PinchIn', 'PinchOut', 'ThumbUp', 'ThumbDown',
            'ExtendedHandStart', 'ExtendedHandEnd', 'None']

class DataCollectorModel:
    def __init__(self, cam_ids, selected_gesture, record_time, save_dir):   
        cameras = []
        for id in cam_ids:
            cameras.append(cv2.VideoCapture(id))
        
        frames = []
        for cam in cameras: 
            _, frame = cam.read()
            frames.append(frame)
        
        hands = []
        for cam in cameras:
            hands.append(mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.95))
        
        self.columnames = []
        for i in range(NUM_HAND_LANDMARKS):
            self.columnames.append("x{}".format(i))
            self.columnames.append("y{}".format(i)) 
            self.columnames.append("z{}".format(i))
        self.columnames.append("gesture")
        
        self.cameras = cameras
        self.frames = frames
        self.hands = hands
        self.selected_gesture = selected_gesture
        self.record_time = record_time
        self.save_dir = save_dir
        self.test_model_dir = '../models/knn.pkl'
        self.test_mode = False
        self.mpHands = mp.solutions.hands
        self.mpDraw = mp.solutions.drawing_utils  
        self.is_recording = False
        self.gesture_types = GESTURES
        self.gestures_df = pd.DataFrame(columns=self.columnames)

    
    @property
    def cameras(self):
        return self.__cameras
    @cameras.setter
    def cameras(self, cameras):
        self.__cameras = cameras

    @property
    def selected_gesture(self):
        return self.__selected_gesture
    @selected_gesture.setter
    def selected_gesture(self, selected_gesture):
        if selected_gesture in GESTURES:
            self.__selected_gesture = selected_gesture
        else:
            raise ValueError(f'Invalid gesture: {selected_gesture}')

    @property
    def record_time(self):
        return self.__record_time
    @record_time.setter
    def record_time(self, record_time):
        try:
            self.__record_time = int(record_time)
        except:
            raise ValueError(f'Invalid record time: {record_time}')

    @property
    def save_dir(self):
        return self.__save_dir
    @save_dir.setter
    def save_dir(self, save_dir):
        if os.path.exists(save_dir):
            self.__save_dir = save_dir
        else:
            raise ValueError(f'Invalid saving directory: {save_dir}')
    
    @property
    def model_dir(self):
        return self.__model_dir
    @model_dir.setter
    def model_dir(self, model_dir):
        if os.path.exists(model_dir):
            self.__model_dir = model_dir
        else:
            raise ValueError(f'Invalid mdoel directory: {model_dir}')

    @property
    def test_mode(self):
        return self.__test_mode
    @test_mode.setter
    def test_mode(self, test_mode):
        self.__test_mode = test_mode
           
    @property
    def is_recording(self):
        return self.__is_recording
    @is_recording.setter
    def is_recording(self, is_recording):
        self.__is_recording = is_recording

    @property
    def gestures_df(self):
        return self.__gestures_df
    @gestures_df.setter
    def gestures_df(self, gestures_df):
        self.__gestures_df = gestures_df

    def add_gesture_series(self, dots, gesture):
        data = []
        for dot in dots:
            data.append(dot[0])
            data.append(dot[1])
            data.append(dot[2])
        data.append(gesture)
       
        df_row = pd.Series(data=data, index=self.gestures_df.columns)
        self.gestures_df = pd.concat([self.gestures_df, pd.DataFrame([df_row])], ignore_index=False, axis=0)

    def update_hands(self):
        hands = []
        for _ in range(len(self.cameras)):
            hands.append(mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.95))
        self.hands = hands


