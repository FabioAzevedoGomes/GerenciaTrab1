import Tkinter as tk

class ApplicationFrame(tk.Frame):
    """The main application frame"""
    
    def __init__(self, parent,  *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title('Application')
        self.parent.resizable(False, False)
        self.initialize()
        
    def initialize(self):
        pass
