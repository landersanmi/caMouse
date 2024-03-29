import numpy as np
import pandas as pd

from os.path import exists

from models.GestureEnum import Gesture


class DataCheckModel:
    
    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        self._frame = value

    @property
    def frame_masked(self):
        return self._frame_masked

    @frame_masked.setter
    def frame_masked(self, value):
        self._frame_masked = value

    @property
    def plot(self):
        return self._plot

    @plot.setter
    def plot(self, value):
        self._plot = value

    @property
    def plot_toogle(self):
        return self._plot_toogle

    @plot_toogle.setter
    def plot_toogle(self, value):
        self._plot_toogle = value

    @property
    def gesture(self):
        return self._gesture

    @gesture.setter
    def gesture(self, value):
        self._gesture = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
    
    @property
    def hand_normalized_cords(self):
        return self._hand_normalized_cords

    @hand_normalized_cords.setter
    def hand_normalized_cords(self, value):
        self._hand_normalized_cords = value

    @property
    def hand_pre_cords(self):
        return self._hand_pre_cords

    @hand_pre_cords.setter
    def hand_pre_cords(self, value):
        self._hand_pre_cords = value

    @property
    def hand_real_coords(self):
        return self._hand_real_coords

    @hand_real_coords.setter
    def hand_real_coords(self, value):
        self._hand_real_coords_pre = np.copy(self._hand_real_coords)
        self._hand_real_coords = value

    @property
    def hand_cords(self):
        return self._hand_cords

    @property
    def hand_cords_expanded(self):
        if self._hand_cords is None:
            return None
        return [p for pair in self._hand_cords for p in pair]

    @hand_cords.setter
    def hand_cords(self, value):
        self._hand_cords = value

    @property
    def hand_dataset(self):
        return self._hand_dataset

    @hand_dataset.setter
    def hand_dataset(self, value):
        self.hand_dataset = value

    def __init__(self, db = "data/hand_dataset.csv", history = "data/history.csv"):
        self._frame = None
        self._frame_masked = None
        self.plot = None
        self._plot_toogle = True

        self._status = None
        self._gesture = None

        self._hand_cords = None
        self._hand_pre_cords = None
        
        self._hand_normalized_cords = None
        
        self._hand_real_coords = None
        self._hand_real_coords_pre = None
        
        self._hand_dataset = None
        self.history = pd.read_csv(history)
        self.load_dataset(db)

    def add_hand_model(self):
        list_coords = [self._gesture]
        list_coords += [p for pair in self._hand_cords for p in pair]
        self._hand_dataset.loc[len(self._hand_dataset)] = list_coords

    def load_dataset(self, db = None):
        if db is None or not exists(db):
            print("Creating new dataframe")
            self._hand_dataset = pd.DataFrame(columns = ["Category"] + [str(i) for i in range(21*3)])
        else:
            print("Using base dataset")
            self._hand_dataset = pd.read_csv(db)

    def get_action_counts(self):
        return [self.get_action_count(i) for i in range(len(Gesture))]

    def get_action_count(self, action):
        return len(self._hand_dataset[self._hand_dataset["Category"] == action])