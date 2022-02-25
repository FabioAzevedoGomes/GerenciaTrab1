from step import Step
from GUI.login import LoginFrame
from globals import root

class LoginStep(Step):
    """The application login step"""
    
    def execute(self, data=None):
        global root
        LoginFrame(parent=root, connect_function=self._complete)
        root.mainloop()

    def _complete(self, data, callback):
        data['login_success_callback'] = callback
        self.complete(data)
