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
        # TODO Implement the direction function
        self.prev_position = hand_model

        raise NotImplementedError("Direction of hand is not yet implemented.")

    def step(self, hand_model) -> None:
        if not self.is_active():
            return
        
        print("-----------")
        
        # TODO Maybe add the frame to hand detector here
        action, _ = self.model(hand_model)
        print(f"Got action {action}")

        state = self.action_graph.step(action)
        print(f"Moving to state {action}")

        self.mouse.apply_state(state)

        if self.action_graph.is_currently_moveable():
            self.mouse.move_mouse(self.get_direction(hand_model))

