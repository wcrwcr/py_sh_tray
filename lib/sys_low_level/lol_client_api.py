import requests as http
from requests.auth import HTTPBasicAuth
from lib import client_checker
from requests.packages.urllib3.exceptions import InsecureRequestWarning

http.packages.urllib3.disable_warnings(InsecureRequestWarning)



class Error(Exception):
    pass

class ApiNotReady(Error):
    pass
    #def __init__(self, expression, message):
    #    self.expression = expression
    #    self.message = message

class LolClientApi():
    connectionString = "{1!s}://127.0.0.1:{0!s}"

    def __init__ (self, port, pwd, protocol="https"):
        clientIsUp = client_checker.Client_Checker().checkAvail()
            
        #print('api', clientIsUp)
        try:
            
            if not port or not pwd or not clientIsUp:
                raise ApiNotReady("we have no data avail")
            self.connectionString = self.connectionString.format(port, protocol)
            self.auth = HTTPBasicAuth('riot', pwd)
        except (ApiNotReady) as err:
            print (err)
    
    def formUri(self, path):
        return self.connectionString + path
    
    def getRequest(self, uri):
        #print(self.formUri(uri))
        #print(self.auth)
        r = http.get(self.formUri(uri), auth=self.auth, verify=False)
        if (r.status_code == 200):
            #print(f'responce for {uri} : {r.json()}')
            return r.json()
        
        print(f'request failed [{r.status_code}] for \'{uri}\'')
        return None
        
        
            