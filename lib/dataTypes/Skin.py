''''data type summoner'''
from lib.dataTypes.jsonDefinedData import jsonDefinedData

from var_dump import var_dump

class Skin(jsonDefinedData):
    
    id = None 
    name = None
    
    def __init__(self, data):
        super(Skin, self).__init__(data)
        self.id = self._json['id']
        self.name = self._json['name']
        #var_dump(self._json)
    
    def isOwned(self):
        return (not self._json['isBase']) and self._json['ownership']['owned']
    
    def __str__(self):
        return f"Skin #{self.id} `{self.name}`"
    
    def export(self):
        return {self.name : self}
