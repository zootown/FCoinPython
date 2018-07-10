import configparser
import threading
import websocket
import json

cf = configparser.ConfigParser()
cf.read("fcoin.ini")
key = cf.get("Key", "Public")
secret = cf.get("Key", "Secret")
websocket.enableTrace(False)

class DepthWsClass(threading.Thread):
    def __init__(self, fc):
        threading.Thread.__init__(self)
        self.fc = fc

    def run(self):
        self.fc.DepthLock.acquire()
        if self.fc.DepthWs != None:
            self.fc.DepthWs.close()
            self.fc.DepthWs = None
        self.fc.DepthWs = websocket.WebSocketApp("wss://ws.fcoin.com/api/v2/ws",
                                         on_message=self.fc.on_DepthMessage,
                                         on_error=self.fc.on_DepthError,
                                         on_close=self.fc.on_DepthClose)
        self.fc.DepthWs.on_open = self.fc.on_DepthOpen
        print("try to Open Depth", end="\n")
        self.fc.DepthLock.release()
        self.fc.DepthWs.run_forever()


class TASWsClass(threading.Thread):
    def __init__(self, fc):
        threading.Thread.__init__(self)
        self.fc = fc

    def run(self):
        self.fc.TASLock.acquire()
        if self.fc.TasWs != None:
            self.fc.TasWs.close()
            self.fc.TasWs = None
        self.fc.TasWs = websocket.WebSocketApp("wss://ws.fcoin.com/api/v2/ws",
                                       on_message=self.fc.on_TasMessage,
                                       on_error=self.fc.on_TasError,
                                       on_close=self.fc.on_TasClose)

        self.fc.TasWs.on_open = self.fc.on_TasOpen
        print("try to Open TAS", end="\n")
        self.fc.TASLock.release()
        self.fc.TasWs.run_forever()


class FCoinWsClass():
    def __init__(self,symbol):
        self.symbol=symbol
        self.DepthLock=threading.Lock()
        self.TASLock = threading.Lock()
        self.TAS = threading.Lock()
        self.DepthWs = None
        self.TasWs = None
        self.DepthThread = None
        self.TASThread = None
        self.StartDepthWs()
        self.StartTASWs()

    def StopStartDepthWs(self):
        if self.DepthWs != None:
            self.DepthWs.close()
            self.DepthWs = None
        if self.DepthThread != None:
            self.stop()

    def StartDepthWs(self):
        DepthThread = DepthWsClass(self)
        DepthThread.start()

    def StartTASWs(self):
        TASThread = TASWsClass(self)
        TASThread.start()

    def on_TasMessage(self, ws, message):
        #print(message)
        pass

    def on_DepthMessage(self, ws, message):
        #print(message)
        pass

    def on_DepthError(self, ws, error=None):
        print("Depth error:" + str(error), end="\n")

    def on_DepthClose(self, ws):
        print("Depth closed:" + str(ws), end="\n")
        self.StartDepthWs(self)

    def on_DepthOpen(self, ws):
        print("Depth open:" + str(ws), end="\n")
        s = "depth.L20.{}".format(self.symbol)
        req = {
            'cmd': 'sub',
            'args': [s],
        }
        cmd = json.dumps(req)
        ws.send(json.dumps(req))

    def on_TasError(self, ws, error=None):
        ws.close()
        print("TAS error:" + str(error), end="\n")

    def on_TasClose(self, ws):
        print("TAS closed:" + str(ws), end="\n")
        self.StartTASWs(self)


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
    fc= FCoinWsClass('ftusdt')