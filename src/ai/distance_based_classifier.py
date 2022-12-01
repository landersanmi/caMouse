
import numpy as np

class DistanceBasedClassifier:
    
    def __init__(self, eps = 0.1):
        self.eps = eps
        self.hand_actions = []
    
    def add_hand_action(self, hand_rack, category):
        self.hand_actions += (hand_rack, category)
    
    def predict(self, hand_rack):
        min_distance = -1
        best_action = None
        for possible_action in self.hand_actions:
            
            distance = np.linalg.norm(possible_action[0] - hand_rack)
            if distance < min_distance or best_action is None:
                min_distance = distance
                best_action = possible_action[1]
                
        return best_action
                