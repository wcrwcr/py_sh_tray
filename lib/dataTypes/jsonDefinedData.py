
import json
import datetime
import decimal

class jsonDefinedData():
    _rawJson = None
    _json = None
    
    def __init__(self, data):
        self._json = data
        self.toJson()
        
    def toData(self):
        self._json = json.JSONDecoder().decode(self._rawJson)
        return self._json
        
    def toJson(self):
        self._rawJson = json.JSONEncoder().encode(self._json)
        return self._rawJson
    
    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            if isinstance(value, datetime.datetime):
                iso = value.isoformat()
                yield attr, iso
            elif isinstance(value, decimal.Decimal):
                yield attr, str(value)
            elif(hasattr(value, '__iter__')):
                if(hasattr(value, 'pop')):
                    a = []
                    for subval in value:
                        if(hasattr(subval, '__iter__')):
                            a.append(dict(subval))
                        else:
                            a.append(subval)
                    yield attr, a
                else:
                    yield attr, dict(value)
            else:
                yield attr, value
    
    def toJSON2(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
