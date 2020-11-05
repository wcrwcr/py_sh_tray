from json import JSONEncoder
from var_dump import var_dump
''' tbd: decide if any '_' prefix vars shd be removed '''

class jsonDump(JSONEncoder):
    def default(self, o):
        z= o.__dict__
        z.pop('_rawJson', None)
        #for item in z:
            #var_dump(item)
        return z