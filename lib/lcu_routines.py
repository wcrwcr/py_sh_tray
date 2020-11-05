''' this is async listener, may be required to listen to events in profile later '''

from lcu_driver import Connector

class LCU():

    connector = None


        
    
    def __init__(self):
        
        self.connector = Connector()
        self.run_window()
        
        @self.connector.ready
        async def connect(connection):
            print('LCU API is ready to be used.')
            summoner = await connection.request('get', '/lol-summoner/v1/current-summoner')
            print(await summoner.json())

    
        @self.connector.ws.register('/lol-summoner/')
        async def eventlist(connection, event):
            print(f'lcu event {event.data} was fired.')

        @self.connector.close
        async def disconnect(connection):
            print('The client was closed')
            await self.connector.stop()
    
        self.connector.start()