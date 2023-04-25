from speedometer import Speedometer
import asyncio
from server_malworking import UDPserver

class mainApp:
    #vel = 0
    def __init__(self):
        self.velo = 0
        self.queue= asyncio.Queue(0)

    async def server(self):
        while True:
            self.velo= UDPserver.mainLoopUDPserver()
            print("THIS IS VELO{}",self.velo)
            #await self.queue.put(self.velo)

            #vel= await self.queue.get()
            #return vel
            #print("ASSDASDSADSD{}",vel)

            await asyncio.sleep(0)
            #print("HI, vel Received={}",self.veloc)
        #return velo

    async def widget(self):
        while True:
            #vel =  await self.queue.get()
            #print("Hola xDDDDDDD", vel)
            print(">>>>>>>>>>>>>>>NextIteration>>>>>>>>>>>>>>")
            await Speedometer.mainLoopSpd()
            await asyncio.sleep(0)


loop= asyncio.get_event_loop()
mApp= mainApp()

loop.create_task(mApp.server())
loop.create_task(mApp.widget())
loop.run_forever()