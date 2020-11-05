import psutil
import pathlib

CLIENT_APP_NAME = 'LeagueClient.exe'
CLIENT_LOCKFILE_NAME = 'lockfile'

class Error(Exception):
    pass

class FileError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class FileEmpty(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
                
class NoData(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
                        
class Windows():
    client_port = ""
    client_pwd = ""
    
    def __init__(self):
        self.osType = "win"
    
    def checkLolUp(self):
        for p in psutil.process_iter():
            if p.name() == CLIENT_APP_NAME:
                if self.getBearer(p):
                    return True
        return False
    
    def getBearer(self, process):
        if self.client_port and self.client_pwd:
            return True
        try:
            file = pathlib.Path(process.cwd()).joinpath(CLIENT_LOCKFILE_NAME)
            if not file.exists ():
                raise FileError (file + " is not exist")
            fileData = file.read_text()
            if not fileData:
                raise FileEmpty ("lockfile has no data")
            sortedData = fileData.split(":")
            if not sortedData[2] or not sortedData[3]:
                raise NoData("locfile can not be parsed")
            self.client_port = sortedData[2]
            self.client_pwd = sortedData[3]
            return True
        
        except (FileError, FileEmpty, NoData) as err:
            print (err)
        

        return False

        