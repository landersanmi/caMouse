
class MouseController:
    def __init__(self) -> None:
        pass

    def move_mouse(self, direction):
        """
            Direction : Tuple (float, float) Represents (x,y) direction
        """
        raise NotImplementedError("Move mouse is not yet implemented.")

    def apply_state(self, action):
        if action == 0:
            pass
        if action == 1:
            pass
        if action == 2:
            # Click
            pass
        # TODO Hacer un switch aqui
