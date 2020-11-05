''''data type summoner'''
from lib.dataTypes.jsonDefinedData import jsonDefinedData

class Summoner(jsonDefinedData):
    
    id = None 
    name = None
    icon = None
    puuid = None
    
    def __init__(self, data):
        super(Summoner, self).__init__(data)
        self.id = self._json['summonerId'] #unique id for user IN region 
        self.name = self._json['displayName']
        self.icon = self._json['profileIconId']
        self.puuid = self._json['puuid'] #unique id for user\region
    