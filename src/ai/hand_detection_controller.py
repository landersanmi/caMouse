from graph.graph import ActionGraph

from mouse.mouse_controler import MouseController

class HandDetectionController:
    def __init__(self, model = None) -> None:
        self.action_graph = ActionGraph("base")
        self.model = model

        self._is_active = False

        self.mouse = MouseController()

        self.prev_position = None

    def is_active(self):
        return self._is_active

    def set_active(self, state):
        self._is_active = state

    def get_direction(self, hand_model):
        if self.prev_position is None:
            self.prev_position = hand_model
            return None
        
        direction = (
            int(6000*(self.prev_position[5, 0] - hand_model[5, 0])),
            int(6000*(self.prev_position[5, 1] - hand_model[5, 1]))
        )
        self.prev_position = hand_model
        
        return direction

    def step(self, hand_model_normalized, hand_model_real) -> None:
        if not self.is_active() or hand_model_normalized is None:
            return
        
        print("-----------")
        # TODO Maybe add the frame to hand detector here
        action, _ = self.model(hand_model_normalized)
        print(f"Got action {action}")

        state = self.action_graph.step(action)
        print(f"Moving to state {state}")

        self.mouse.apply_state(state)
        if self.action_graph.is_currently_moveable():
            direction = self.get_direction(hand_model_real)
            
            if direction is not None:
                try:
                    self.mouse.move_mouse(direction)
                except:
                    print("Not possible move")
