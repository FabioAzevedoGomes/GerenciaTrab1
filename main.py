from Steps.application_step import ApplicationStep
from Steps.login_step import LoginStep
from Steps.connect_step import ConnectStep

if __name__ == '__main__':
    login = LoginStep()
    connect = ConnectStep()
    application = ApplicationStep()
    
    login.then(connect.then(application)).execute()
    