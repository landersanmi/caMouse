from PIL import Image, ImageTk
import tkinter as tk
import cv2
import numpy as np
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import time

import mediapipe as mp

import logging

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

from ai.distance_based_classifier import DistanceBasedClassifier
from ai.hand_detection_controller import HandDetectionController

HAND_CONNECTIONS = [(0, 1), (0, 5), (0, 17), (1, 2), (2, 3), (3, 4), (5, 6), (5, 9), 
                    (6, 7), (7, 8), (9, 10), (9, 13), (10, 11), (11, 12), (13, 14), 
                    (13, 17), (14, 15), (15, 16), (17, 18), (18, 19), (19, 20)]

def rotation_matrix_from_vectors(vec1, vec2):
    """ Find the rotation matrix that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
    """
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
    return rotation_matrix

class DataCheckController:
    def __init__(self, model, view, use_camera = True):
        self.model = model
        self.view = view

        self.use_camera = use_camera

        
        self.view.refresh_count(self.model.get_action_counts())

        self.classifier = DistanceBasedClassifier(eps = 0.2)
        print(self.model.hand_dataset.head())
        df = self.model.hand_dataset
        for ind in df.index:
            line = df.loc[ind].tolist()
            action = line[0]
            rack = line[1:]
            self.classifier.add_hand_action(rack, action)
            
        
        self.mouse_controller = HandDetectionController(model = self.classifier)
        self.mouse_controller.set_active(True)
        self.mouse_time = 0


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

        

        self.view.refresh_count(self.model.get_action_counts())

        self.model.hand_dataset.to_csv("data/hand_dataset.csv", index=False)

        self.classifier.add_hand_action(self.model.hand_cords_expanded, self.model.gesture)


    def capture_cam(self):
        if self.source is not None:
            status, frame = self.source.read()
            

            self.model.status = status
            self.model.frame = frame
            
            self.get_hand()
            self.detect_hand()

            frame = cv2.flip(frame, 1)

            self.model.frame_masked = np.copy(frame)

            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)

            self.view.frame.image = imgtk
            self.view.frame.configure(image=imgtk)
            self.view.frame.update()
            self.view.frame.after(10, self.capture_cam)

    def detect_hand(self):
        
        self.mouse_time += 1
        
        if self.model.hand_cords is not None:
            action, distance = self.classifier.predict(self.model.hand_cords_expanded)
            self.view.distance.config(text = "Distance : " + str(distance)[:4])
            self.view.category.config(text = "Category : " + str(action))
        
            #if self.mouse_time % 20 == 0:
            if self.mouse_controller.is_active():
                self.mouse_controller.step(
                    self.model.hand_cords_expanded, 
                    self.model.hand_real_coords)
            
                #coordinates = [x for sublist in self.model.hand_real_coords for x in sublist]

                #self.save_step(coordinates, action)
        

    def get_hand(self, tridimensional = False):
        frame = self.model.frame
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(framergb)

        x , y, c = frame.shape

        landmarks=[]
        dots = np.empty((0,3), int)

        if result.multi_hand_landmarks:
            for handslms in result.multi_hand_landmarks:
                x, y, z = [], [], []
                for i, lm in enumerate(handslms.landmark):
                    dots = np.append(dots, [[lm.x, lm.y, lm.z]] , axis=0)
                    x.append(lm.x)
                    y.append(lm.y)
                    z.append(lm.z)
                    
                self.model.hand_real_coords = np.copy(dots)
                dots_relocated = dots[0]-dots 
                
                # Rotate to certain position
                q = rotation_matrix_from_vectors(np.array((0,1,0)), np.array(dots_relocated[5]))
                
                new_dots = [np.array((0,0,0))]

                for dot in dots_relocated[1:]:
                    new_dots += [np.array(dot).dot(q)]

                custom_dot = np.array((new_dots[17][0],0,new_dots[17][2]))
                q2 = rotation_matrix_from_vectors(np.array((np.linalg.norm(custom_dot),0,0)), custom_dot)
                
                new_dots2 = [np.array((0,0,0))]
                for i, dot in enumerate(new_dots[1:]):
                    new_dots2 += [np.array(dot).dot(q2)]
                new_dots2 = np.array(new_dots2)

                new_dots2[:, 1] /= new_dots2[5][1]
                new_dots2[:, 1] *= 0.1
                new_dots2[:, 0] /= new_dots2[17][0]
                new_dots2[:, 0] *= 0.05

                
                self.model.hand_pre_cords = np.copy(self.model.hand_cords)

                self.model.hand_cords = np.array(new_dots2)
                #self.model.hand_normalized_cords = dots_relocated


                self.mpDraw.draw_landmarks(frame, handslms, self.mpHands.HAND_CONNECTIONS)
                
                '''
                cv2.circle(frame, (int(200+new_dots2[0][0]*400), int(200+400*new_dots2[0][1])), 1, (255,255,0),2)
                cv2.circle(frame, (int(200+new_dots2[5][0]*400), int(200+400*new_dots2[5][1])), 1, (255,0,255),2)
                cv2.circle(frame, (int(200+new_dots2[17][0]*400), int(200+400*new_dots2[17][1])), 1, (255,127, 127),2)
                for i, dot in enumerate(new_dots2):
                    if i in [0, 5, 17]:
                        continue
                    cv2.circle(frame, (int(200+dot[0]*400), int(200+400*dot[1])), 1, (255,0,0),2)

                    
                cv2.circle(frame, (int(100+dots_relocated[0][0]*400), int(100+400*dots_relocated[0][1])), 1, (255,255,0),2)
                cv2.circle(frame, (int(100+dots_relocated[5][0]*400), int(100+400*dots_relocated[5][1])), 1, (255,0,255),2)
                cv2.circle(frame, (int(100+dots_relocated[17][0]*400), int(100+400*dots_relocated[17][1])), 1, (255,127, 127),2)
                for i, dot in enumerate(dots_relocated):
                    if i in [0, 5, 17]:
                        continue
                    cv2.circle(frame, (int(100+dot[0]*400), int(100+400*dot[1])), 1, (255,0,0),2)
                    

                cv2.circle(frame, (int(300+new_dots[0][0]*400), int(300+400*new_dots[0][1])), 1, (255,255,0),2)
                cv2.circle(frame, (int(300+new_dots[5][0]*400), int(300+400*new_dots[5][1])), 1, (255,0,255),2)
                cv2.circle(frame, (int(300+new_dots[17][0]*400), int(300+400*new_dots[17][1])), 1, (255,127, 127),2)
                for i, dot in enumerate(new_dots):
                    if i in [0, 5, 17]:
                        continue
                    cv2.circle(frame, (int(300+dot[0]*400), int(300+400*dot[1])), 1, (255,0,0),2)
                '''
                
                if len(x) != 0: 
                    if self.model.plot_toogle:
                        '''
                        plot = self.generate_3D_plot(x, y, z)
                        tk_hand_image = ImageTk.PhotoImage(Image.fromarray(plot))
                        self.view.plot.configure(image=tk_hand_image)
                        self.view.plot.image = tk_hand_image
                        '''
        else:
            self.model.hand_cords = None      
        self.model.frame = frame

    def change_gesture(self):
        gesture_type = self.view.opcion.get()
        self.model.gesture = gesture_type

    def set_frame(self, frame):
        # save the model
        self.model.frame = frame

    def toggle_mouse_controller(self):
        self.model.plot_toogle = not self.model.plot_toogle
        self.mouse_controller.set_active(self.model.plot_toogle)
        print(f"Current mouse state {self.mouse_controller.is_active()}.")
    
    def generate_3D_plot(self, x, y, z):

        plt.close('all')
        fig = plt.figure(figsize=(8, 8), dpi=35)
        canvas = FigureCanvasAgg(fig)
        ax = plt.axes(projection='3d')
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

    def save_step(self, hand_model, state):
        row = pd.Series([state] + hand_model, index=self.model.history.columns, name=1)
        self.model.history = self.model.history.append(row)
        self.model.history.to_csv("data/history.csv", sep=',', index=False)