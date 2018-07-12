import threading
import websockets
import json
import asyncio

class DepthWsClass(threading.Thread):
    def __init__(self, fc):
        threading.Thread.__init__(self)
        self.fc = fc

    async def wsthread(self):
        async with websockets.connect('wss://ws.fcoin.com/api/v2/ws') as websocket:
            print("DepthOpened")
            response = await websocket.recv()
            s = "depth.L20.{}".format("ftusdt")
            req = {
                'cmd': 'sub',
                'args': [s],
            }
            cmd = json.dumps(req)
            await websocket.send(cmd)
            while True:
                response = await websocket.recv()
                data=json.loads(response)
                if "bids" in data:
                    self.fc.on_DepthMessage(websocket,data)

    def run(self):
        asyncio.new_event_loop().run_until_complete(self.wsthread())
        self.fc.on_DepthClose(None)

class TASWsClass(threading.Thread):
    def __init__(self, fc):
        threading.Thread.__init__(self)
        self.fc = fc

    def run(self):
        with self.fc.TASLock:

            self.fc.TasWs.on_open = self.fc.on_TasOpen
            print("try to Open TAS", end="\n")
        self.fc.TasWs.run_forever()


class FCoinWsClass():
    def __init__(self,symbol):
        self.symbol=symbol
        self.DepthLock=threading.RLock()
        self.TASLock = threading.RLock()
        self.DepthWs = None
        self.TasWs = None
        self.DepthThread = None
        self.TASThread = None
        self.DepthActions=set()
        self.TASActions=set()

    def Close(self):
        self.StopDepthWs()
        self.StopTAShWs()

    def AddDepthAction(self,action):
        with self.DepthLock:
            if not self.DepthIsOpen():
                self.StartDepthWs()
            self.DepthActions.add(action)

    def RemoveDepthAction(self,action):
        with self.DepthLock:
            try:
                self.DepthActions.remove(action)
            except:
                print("RemoveDepthActionError")
            if len(self.DepthActions) < 1:
                self.StopDepthWs()

    def AddTASAction(self,action):
        with self.TASLock:
            if not self.TASIsOpen():
                self.StartTASWs()
            self.TASActions.add(action)

    def RemoveTASAction(self,action):
        with self.TASLock:
            try:
                self.TASActions.remove(action)
            except:
                print("RemoveDepthActionError")
            if len(self.TASActions) < 1:
                self.StopTAShWs()

    def DepthIsOpen(self):
        with self.DepthLock:
            return self.TasWs != None

    # 此处不Lock，注意
    def TASIsOpen(self):
        with self.TASLock:
            return self.DepthWs != None

    def StopTAShWs(self):
        with self.TASLock:
            if self.TASIsOpen():
                self.TasWs.close()
                self.TasWs = None

    def StopDepthWs(self):
        with self.DepthLock:
            if self.DepthIsOpen():
                self.DepthWs.close()
                self.DepthWs = None

    def StartDepthWs(self):
        self.StopDepthWs()
        DepthThread = DepthWsClass(self)
        DepthThread.start()

    def StartTASWs(self):
        self.StopTAShWs()
        TASThread = TASWsClass(self)
        TASThread.start()

    def on_TasMessage(self, ws, message):
        with self.TASLock:
            actions=self.TASActions.copy()
            for cur in actions:
                cur(message)
        pass

    def on_DepthMessage(self, ws, message):
        with self.DepthLock:
            actions=self.DepthActions.copy()
            for cur in actions:
                cur(message)
        pass

    def on_DepthError(self, ws, error):
        print("Depth error:" + str(error), end="\n")

    def on_DepthClose(self, ws):
        print("Depth closed:" + str(ws), end="\n")
        self.StartDepthWs()

    def on_DepthOpen(self, ws):
        print("Depth open:" + str(ws), end="\n")
        s = "depth.L20.{}".format(self.symbol)
        req = {
            'cmd': 'sub',
            'args': [s],
        }
        cmd = json.dumps(req)
        ws.send(cmd)

    def on_TasError(self, ws, error):
        ws.close()
        print("TAS error:" + str(error), end="\n")

    def on_TasClose(self, ws):
        print("TAS closed:" + str(ws), end="\n")
        self.StartTASWs()


    def on_TasOpen(self, ws):
        print("TAS open:" + str(ws), end="\n")
        s = "ticker.{}".format(self.symbol)
        req = {
            'cmd': 'sub',
            'args': [s],
            'id': '1'
        }
        ws.send(json.dumps(req))






if __name__== '__main__':
    print("11")