''''data type summoner'''
from lib.dataTypes.jsonDefinedData import jsonDefinedData

from var_dump import var_dump

class Champion(jsonDefinedData):
    
    id = None 
    name = None
    skins = None
    items = None
    
    def __init__(self, data):
        super(Champion, self).__init__(data)
        self.id = self._json['id']
        self.name = self._json['name']
        self.skins = {}
        self.items = {}
    
    def isOwned(self):
        return self._json['ownership']['owned']
    
    def addSkin(self, skin):
        self.skins.update({skin.name:skin})
    
    def addItems(self, items):
        self.items.update({items.id:items})
            
    def __str__(self):
        return f"Chamion #{self.id} `{self.name}` with `{len(self.skins)}`"
    