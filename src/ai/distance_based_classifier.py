
import numpy as np

class DistanceBasedClassifier:
    
    def __init__(self, eps = 0.1):
        self.eps = eps
        self.hand_actions = []
    
    def add_hand_action(self, hand_rack, category):
        self.hand_actions += [(hand_rack, category)]
    
    def __call__(self, hand_rack):
        return self.predict(hand_rack)
    
    def predict(self, hand_rack):
        if hand_rack is None:
            return None, -1
        
        min_distance = -1
        best_action = None
        for possible_action in self.hand_actions:
            distance = np.linalg.norm(np.array(possible_action[0]) - np.array(hand_rack))
            if distance < min_distance or best_action is None:
                min_distance = distance
                best_action = possible_action[1]
                
        return best_action, min_distance
                