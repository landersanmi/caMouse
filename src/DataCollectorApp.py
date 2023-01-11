import tkinter as tk
from controllers.DataCollectorController import DataCollectorController
from views.DataCollectorView import DataCollectorView
from models.DataCollectorModel import DataCollectorModel
import threading

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Hand Gestures data colector')
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.geometry("2500x1380")
        self.state('zoomed') 

        self.call("source", "themes/azure.tcl")
        self.call("set_theme", "light")

        cameras = [0, 'http://192.168.0.16:4747/video']
        model = DataCollectorModel([], 'None', 5, 'C:/')
       
        view = DataCollectorView(self)

        controller = DataCollectorController(model, view)
        view.set_controller(controller)
        
        for _ in range(controller.get_cam_count()):
            view.add_cam_frame()   
        
        camera_thread = threading.Thread(target=view.update_cameras_loop)
        camera_thread.start()

if __name__ == '__main__':
    app = App()
    app.mainloop()   
    app.destroy()