from PIL import Image, ImageTk
import tkinter as tk
import cv2
import numpy as np

import time

import mediapipe as mp

import logging

from ai.distance_based_classifier import DistanceBasedClassifier

class DataCheckController:
    def __init__(self, model, view, use_camera = True):
        self.model = model
        self.view = view

        self.use_camera = use_camera

        self.classifier = DistanceBasedClassifier(eps = 1000000000)

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(max_num_hands=1, min_detection_confidence=0.8)
        self.mpDraw = mp.solutions.drawing_utils

        if self.use_camera:
            print("Capturing cam.")
            self.load_camera()
        else:
            print("Using image.")
            self.model.frame = np.zeros((480, 720, 3)).astype(np.uint8)
            img = Image.fromarray(np.zeros((480, 720, 3)).astype(np.uint8))
            imgtk = ImageTk.PhotoImage(image=img)
            self.view.frame.image = imgtk
            self.view.frame.configure(image=imgtk)
            self.view.frame.update()

        


    def load_camera(self):
        self.source = cv2.VideoCapture(0)

        self.capture_cam()

    def save_image(self):
        time_name = str(int(time.time() * 1000.0))
        logging.info(f"Saving file to snipe_cut_{time_name}.png")
        #cv2.imwrite(f"snipe_cut_{time_name}.png", self.model.frame_masked)
        self.model.add_hand_model()

        self.model.hand_dataset.to_csv("data/hand_dataset.csv")

        self.classifier.add_hand_action(self.model.hand_cords_expanded, self.model.gesture)


    def capture_cam(self):
        if self.source is not None:
            status, frame = self.source.read()
            

            self.model.status = status
            self.model.frame = frame
            
            self.get_hand()
            self.detect_hand()

            self.model.frame_masked = np.copy(frame)

            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)

            self.view.frame.image = imgtk
            self.view.frame.configure(image=imgtk)
            self.view.frame.update()
            self.view.frame.after(10, self.capture_cam)

    def detect_hand(self):
        if self.model.hand_cords is not None:
            action, distance = self.classifier.predict(self.model.hand_cords_expanded)
            self.view.distance.config(text = "Distance : " + str(distance))
            self.view.category.config(text = "Category : " + str(action))
        

    def get_hand(self, tridimensional = False):
        frame = self.model.frame
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(framergb)

        x , y, c = frame.shape

        landmarks=[]
        landmarks_raw = []
        dots = np.empty((0,2), int)

        if result.multi_hand_landmarks:
            for handslms in result.multi_hand_landmarks:
                for i, lm in enumerate(handslms.landmark):
                    lmx, lmy = int(lm.x * x), int(lm.y * y)
                    dots = np.append(dots, [[lmx, lmy]] , axis=0)
                    landmarks_raw.append([lm.x, lm.y, lm.z])
                
                dots_relocated = dots - dots.min(axis=0)

                self.model.hand_pre_cords = np.copy(self.model.hand_cords)

                self.model.hand_cords = dots
                self.model.hand_normalized_cords = dots_relocated


                self.mpDraw.draw_landmarks(frame, handslms, self.mpHands.HAND_CONNECTIONS)

        self.model.frame = frame

    def change_gesture(self):
        gesture_type = self.view.opcion.get()
        self.model.gesture = gesture_type

    def set_frame(self, frame):
        """
        Save the email
        :param email:
        :return:
        """
        # save the model
        self.model.frame = frame

        # show a success message
        self.view.show_success(f'The frame was loaded!')
