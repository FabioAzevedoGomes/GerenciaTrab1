import logging
from step import Step
from Connector.privconnector import PrivConnector
from Connector.noprivconnector import NoPrivConnector

class ConnectStep(Step):
    """The application connection step"""
    
    def execute(self, data=None):
        #logging.info('Login information: ' + str(data))
        
        if 'privacy_protocol' in data:
            connector = PrivConnector()
        else:
            connector = NoPrivConnector()

        connection_data = connector.connect(data)
        data['login_success_callback']()
        self.complete(connection_data)
