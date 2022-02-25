import Tkinter as tk

class ErrorFrame(tk.Toplevel):
    """Error popup"""
    
    def __init__(self, parent, message, *args, **kwargs):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title('Error')
        self.resizable(False, False)

        self.error_label = tk.Label(self, text=message)
        self.error_label.grid(row = 0, column = 0)

        self.ok_button = tk.Button(self, text='OK', command=self.ok_pressed)
        self.ok_button.grid(row = 1, column = 0)

    def ok_pressed(self):
        self.destroy()
