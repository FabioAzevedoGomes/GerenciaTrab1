from step import Step
from GUI.application import ApplicationFrame
from globals import root

class ApplicationStep(Step):
    """The application main menu step"""
    
    def execute(self, data=None):
        global root
        ApplicationFrame(parent = root)
        root.mainloop()

        self.complete(None)
