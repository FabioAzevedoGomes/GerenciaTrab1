from abc import ABCMeta, abstractmethod

class Step():
    __metaclass__ = ABCMeta
    """A step in the application process"""
    
    def __init__(self):
        self.next_step = None
    
    def then(self, next):
        self.next_step = next
        return self

    def complete(self, data=None):
        if (self.next_step):
            self.next_step.execute(data)

    @abstractmethod
    def execute(self, data=None):
        pass
