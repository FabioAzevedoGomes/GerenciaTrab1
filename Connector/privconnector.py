from connector import Connector
from easysnmp import Session
from config import getConfiguration

class PrivConnector(Connector):

    def connect(self, credentials):
        self.session = Session(hostname=getConfiguration('hostname'),
                               version=getConfiguration('version'),
                               security_level='authPriv',
                               auth_protocol=credentials['auth_protocol'],
                               security_username=credentials['username'],
                               auth_password=credentials['password'],
                               privacy_protocol=credentials['privacy_protocol'],
                               privacy_password=credentials['privacy_password'])
        
        print(self.session)
        
        if self.session.error_string:
            raise Exception('Unable to connect to ' + getConfiguration('hostname') + ': ' + self.session.error_string)
        else:
            print(self.session.get('sysName.0'))
