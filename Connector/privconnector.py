from connector import Connector
from easysnmp import Session
from config import getConfiguration
import logging

class PrivConnector(Connector):

    def connect(self, credentials):
        session = Session(hostname=getConfiguration('hostname'),
                               version=getConfiguration('version'),
                               security_level='authPriv',
                               auth_protocol=credentials['auth_protocol'],
                               security_username=credentials['username'],
                               auth_password=credentials['password'],
                               privacy_protocol=credentials['privacy_protocol'],
                               privacy_password=credentials['privacy_password'])
    
        if session.error_string:
            raise Exception('Unable to connect to ' + getConfiguration('hostname') + ': ' + session.error_string)
        else:
            logging.info('Connected privately to ' + session.get('sysName.0').value)

        return session
