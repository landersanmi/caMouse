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

        model = DataColectorModel([], 'None', 5, 'C:/')

        self.geometry("2500x1380")
        self.resizable(0, 0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=7)
        
        view = DataColectorView(self)
        #view.pack(side="left")

        controller = DataColectorController(model, view)
        view.set_controller(controller)
        
        for _ in range(controller.get_cam_count()):
            view.add_cam_frame()   
        
        camera_thread = threading.Thread(target=view.update_cameras_loop)
        camera_thread.start()

if __name__ == '__main__':
    app = App()
    app.mainloop()   
    app.destroy()