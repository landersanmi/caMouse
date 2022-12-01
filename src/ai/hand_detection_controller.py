from graph.graph import ActionGraph

from mouse.mouse_controler import MouseController

class HandDetectionController:
    def __init__(self, model = None) -> None:
        self.action_graph = ActionGraph("base")
        self.model = model

        self.mouse = MouseController()

        self.prev_position = None

    def get_direction(self, hand_model):
        # TODO Implement the direction function
        self.prev_position = hand_model

        raise NotImplementedError("Direction of hand is not yet implemented.")

    def step(self, hand_model) -> None:
        # TODO Maybe add the frame to hand detector here
        action = self.model(hand_model)

        state = self.action_graph.step(action)

        self.mouse.apply_state(state)

        if self.action_graph.is_currently_moveable():
            self.mouse.move_mouse(self.get_direction(hand_model))

