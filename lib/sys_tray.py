import wx.adv
import wx

from lib.sys_low_level import windows
from lib.sys_low_level import lol_client_api
from lib.sys_low_level import jsonDump
from lib import client_checker

from lib.dataTypes import *
from lib.dataTypes.Summoner import Summoner
from lib.dataTypes.Champion import Champion
from lib.dataTypes.Skin import Skin
from lib.dataTypes.Items import Items
from lib.dataTypes.Mission import Mission

from var_dump import var_dump
import json

TRAY_TOOLTIP = 'Smurf Heaven tray' 
TRAY_ICON = 'beemo.png' 

clentMonitor = client_checker.Client_Checker()


class Error(Exception):
    pass

class ApiNotReady(Error):
    pass

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item

class actualRoutines():
    api = None
    #dataBag = None

    def __init__(self, auth):
        self.setAuth(auth)
        self.dataBag = {}
        
    def setAuth(self, data):
        self.port = data['port']
        self.pwd = data['pwd']
        
    def getApi(self):
        try:
            if self.api :
                return self.api
            if not self.port :
                raise ApiNotReady ('cant get port')
            if not self.pwd :
                raise ApiNotReady ('cant get pwd')
            self.api = lol_client_api.LolClientApi(self.port, self.pwd)
            if not self.api.auth :
                raise ApiNotReady ('cant get auth')
            return self.api
            
        except (ApiNotReady) as err:
            print(err)
        return False
     
    def getSummoner(self):
        if self.getApi():
            self.dataBag['summoner'] = Summoner(self.getApi().getRequest('/lol-summoner/v1/current-summoner'))
            if self.dataBag['summoner']:
                return True
        return False 
    
    def getChamps(self):
        if self.getApi():
            self.dataBag['champions'] = []
            zVals = self.getApi().getRequest('/lol-champions/v1/owned-champions-minimal')
            if zVals:
                champsList = {}
                for zChamp in zVals:
                    champ = Champion(zChamp)
                    if champ.isOwned():
                        champsList.update({champ.id: champ})
                self.dataBag['champions'] = champsList
            return len(self.dataBag['champions'])
        return False
    
    def getSkins(self):
        if self.getApi():
            skinCount = 0
            for c_id, champ in self.dataBag['champions'].items():
                zVals = self.getApi().getRequest(f"/lol-champions/v1/inventories/{self.dataBag['summoner'].id}/champions/{champ.id}")
                skinsJson = zVals['skins']
                if skinsJson:
                    for zSkin in skinsJson:
                        skin = Skin(zSkin)
                        if skin.isOwned():
                            self.dataBag['champions'][c_id].skins.update(skin.export())
                            skinCount +=1
                            print(skin)
            return skinCount
                
        return False
    
    def getItems(self):
        if self.getApi():
            itemsetsCount = 0
            zVals = self.getApi().getRequest(f"/lol-item-sets/v1/item-sets/{self.dataBag['summoner'].id}/sets")
            itemsJson = zVals['itemSets']
            
            if itemsJson:
                for zItems in itemsJson:
                    itemSets = Items(zItems)
                    for c_id in itemSets.champions:
                        itemsetsCount += 1
                        if not c_id in self.dataBag['champions'].keys():
                            self.dataBag.update({'unknownItemSets': {c_id: itemSets.export()}})
                        else:
                            self.dataBag['champions'][c_id].items.update(itemSets.export())
                    print(f'{itemSets}')
                return itemsetsCount
        return False
    
    def getMissions(self):
        
        if self.getApi():
            itemsetsCount = 0
            zVals = self.getApi().getRequest(f"/lol-missions/v1/missions")
            if zVals:
                self.dataBag['missions'] = {}
                self.dataBag['missions']['pendingMissions'] = []
                for zMission in zVals:
                    #var_dump(zItems)
                    mis = Mission(zMission)
                    #print (mis)
                    if mis.isActual():
                        series = mis.seriesName
                        if series == '':
                            series = 'unknown'
                        if series not in self.dataBag['missions'].keys():
                            self.dataBag['missions'].update({series: [mis,]})
                        else:
                            self.dataBag['missions'][series].append(mis)
                        if mis.isPending() and not mis.isTFT() and not mis.isTrash():
                            self.dataBag['missions']['pendingMissions'].append(mis)
                            print ('pending mission: ', mis)
                        itemsetsCount +=1
                #var_dump(self.dataBag['missions']['pendingMissions']) #
                #print (f"pending ARE {self.dataBag['missions']['pendingMissions']}")
                return itemsetsCount
        return False
        
        

class TaskBarIcon(wx.adv.TaskBarIcon):
    monitor = None
    
    def gatherData(self):
        if (self.availCheck()):
            if self.router.getSummoner() and self.router.getChamps():
                self.router.getSkins()
                self.router.getItems()
                self.router.getMissions()
                with open('data.txt', 'w') as outfile:
                    json.dump(json.dumps(self.router.dataBag, sort_keys=True, indent=4, cls=jsonDump.jsonDump, ensure_ascii=False), outfile)
                with open('data1.txt', 'w') as outfile:
                    outfile.write(json.dumps(self.router.dataBag, sort_keys=True, indent=4, cls=jsonDump.jsonDump, ensure_ascii=False))
                    #json.dump(json.dumps(self.router.dataBag, sort_keys=True, indent=4, cls=jsonDump.jsonDump, ensure_ascii=False), outfile)
            return True
        return False
        
    def availCheck(self):
        is_up = (windows.Windows().checkLolUp() and self.monitor.checkAvail())
        if is_up :
            self.router = actualRoutines(self.monitor.getLockData())
        else:
            wx.MessageBox("Riot client is not running or logged out", 'LOL client Offline', wx.OK | wx.ICON_EXCLAMATION)
        return is_up 
            
        
    def __init__(self, frame):
        self.monitor = clentMonitor
        '''initial data gather, remove in PR '''
        self.gatherData()   

        
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Sync out', self.on_sync_out)
        create_menu_item(menu, 'Sync in [TBD]', self.on_sync_in)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(path)
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):  
        is_up = self.availCheck()
        print ('LOL instance is {}.'.format("up" if is_up else "down"))
        if is_up:  
            self.gatherData()
        

    def on_sync_out(self, event):
        print ('sync out called')
        self.gatherData()
        

    def on_sync_in(self, event):
        print ('sync in called')

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()

class shTrayApp(wx.App):
    def OnInit(self):
        return self.create_window()
    
    
    def create_window(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True
    
