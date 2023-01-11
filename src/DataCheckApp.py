import tkinter as tk
import threading

from views.DataCheckView import DataCheckView
from models.DataCheckModel import DataCheckModel
from controllers.DataCheckController import DataCheckController

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Hand Gestures analyzer')
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.call("source", "src/themes/azure.tcl")
        self.call("set_theme", "light")

        model = DataCheckModel()
        view = DataCheckView(self)
        controller = DataCheckController(model, view)
        view.set_controller(controller)
        

if __name__ == '__main__':
    app = App()
    app.mainloop()   
    app.destroy()