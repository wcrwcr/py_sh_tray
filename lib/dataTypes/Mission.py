''''data type summoner'''
from lib.dataTypes.jsonDefinedData import jsonDefinedData

from var_dump import var_dump

from datetime import datetime

class Mission(jsonDefinedData):
    
    _now = -1
    
    id = None 
    name = None
    seriesName = None
    description = None
    lastTouch = -1
    endTime = -1
    earnedTime = -1 # time when it was appeared into client
    status = None
    statusText = ""
    
    
    def __init__(self, data):
        super(Mission, self).__init__(data)
        self.id = self._json['id']
        self.name = self._json['title']
        self.description = self._json['description']
        self.seriesName = self._json['seriesName']
        self.lastTouch = self._json['lastUpdatedTimestamp']
        self.endTime = self._json['endTime']
        self.earnedTime = self._json['earnedDate']
        self._now = int(datetime.timestamp(datetime.now())*1000)
        self.statusText = self._json['status']
        self.status = (self.statusText == 'PENDING')
        #var_dump(self._json)
    
    def isActual(self):
        return self.endTime > self._now 
    
    def isTFT(self):
        '''
        non TFT :
        ['display'] => dict(2) 
                ['attributes'] => list(0) 
                ['locations'] => list(0) 
        TFT:
        ['display'] => dict(2) 
                ['attributes'] => list(0) 
                ['locations'] => list(2) 
                    [0] => str(11) "LCU_TRACKER"
                    [1] => str(10) "TFT_WEEKLY"
        
        '''
        for location in self._json['display']['locations']:
            if location in ["TFT_WEEKLY", 'TFT_BATTLEPASS_PROGRESS']:
                return True
        return False
        
    def isTrash(self):
        return self.seriesName in ["clash2020_series", "firstWinOfTheDay"] 
        
    
    def isPending(self):
        return self.status
            
    
    def __str__(self):
        return f"`[{self.seriesName}]{self.name}` Mission (`{self.description}`)"
