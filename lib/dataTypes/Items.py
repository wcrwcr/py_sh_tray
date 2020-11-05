''''data type summoner'''
from lib.dataTypes.jsonDefinedData import jsonDefinedData

from var_dump import var_dump

class Items(jsonDefinedData):
    
    id = None 
    name = None
    champions = []
    maps = []
    slots = []
    type = ""
    mode = ""
    blocks = []
    
    def __init__(self, data):
        super(Items, self).__init__(data)
        self.id = self._json['uid']
        self.name = self._json['title']
        self.champions = self._json['associatedChampions']
        self.maps = self._json['associatedMaps']
        self.slots = self._json['preferredItemSlots']
        self.type = self._json['type']
        self.mode = self._json['mode']
        self.blocks = self._json['blocks']
    
    
    def __str__(self):
        return f"`{self.name}` Itemsets for champ #{self.champions} #`{self.id}`"
    
    def export(self):
        return {self.id : self}
