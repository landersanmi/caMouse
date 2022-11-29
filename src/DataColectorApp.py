import tkinter as tk
from controllers.DataColectorController import DataColectorController
from views.DataColectorView import DataColectorView
from models.DataColectorModel import DataColectorModel
import threading

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Hand Gestures data colector')
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        model = DataColectorModel([], 'LeftClick', 5, 'C:/')

        view = DataColectorView(self)
        view.pack(side="left")

        controller = DataColectorController(model, view)
        view.set_controller(controller)
        
        camera_thread = threading.Thread(target=view.update_cameras_loop)
        camera_thread.start()

if __name__ == '__main__':
    app = App()
    app.mainloop()   