from abc import ABCMeta, abstractmethod

class Connector():
    __metaclass__ = ABCMeta
    """Generic connector for an SNMP agent"""

    @abstractmethod
    def connect(self, credentials):
        pass
