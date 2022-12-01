import tkinter as tk
from views.DataCheckView import DataCheckView
from models.DataCheckModel import DataCheckModel
from controllers.DataCheckController import DataCheckController
import threading

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Hand Gestures analyzer')
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        model = DataCheckModel()

        view = DataCheckView(self)
        #view.pack(side="left")

        controller = DataCheckController(model, view)
        view.set_controller(controller)
        

if __name__ == '__main__':
    app = App()
    app.mainloop()   
    app.destroy()