IS_CLIENT_UP = False
from lib.sys_low_level import windows

class Client_Checker():
    isLolUp = False
    def __init__(self):
        self.isLolUp = False
        
    def checkAvail(self):
        global IS_CLIENT_UP
        self.osRoutines = windows.Windows()
        self.isLolUp = self.osRoutines.checkLolUp()
        IS_CLIENT_UP = self.isLolUp
        return self.isLolUp
    
    def getLockData(self):
        if (self.checkAvail()):
            z= {"port": self.osRoutines.client_port, "pwd": self.osRoutines.client_pwd} 
            print(z)
            return z