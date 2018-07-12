import  fcoin
import threading
import configparser
import time

cf = configparser.ConfigParser()
cf.read("fcoin.ini")
key = cf.get("Key", "Public")
secret = cf.get("Key", "Secret")
api = fcoin.authorize(key, secret)
BalanceThread=None
BalanceLock = threading.RLock()
BalanceActions=set()
OrderThread=None
OrderLock = threading.RLock()
OrderActions=set()
OrderList={}

class BalanceThreadClass(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global api,BalanceThread,BalanceLock,BalanceActions
        print("Balance线程启动")
        try:
            while True:
                Result = api.get_balance()
                with BalanceLock:
                    Actions=BalanceActions.copy()
                if Result != None and "data" in Result:
                    for cur in Actions:
                        cur(Result)
                time.sleep(2.5)
        except:
            with BalanceLock:
                BalanceThread = None
                print("Balance线程异常结束")
                StartBalanceThread()


class OrderThreadClass(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global api, OrderThread, OrderLock, OrderActions,OrderList
        print("Order线程启动")
        try:
            while True:
                TempList = {}
                OldList = OrderList.copy()
                partial_filled = api.list_orders(symbol="ftusdt", states="partial_filled")
                if partial_filled != None and partial_filled["status"] == 0:
                    for CurOrder in partial_filled["data"]:
                        OrderList[CurOrder["id"]] = CurOrder
                        TempList[CurOrder["id"]] = CurOrder
                else:
                    time.sleep(1)
                    continue
                time.sleep(0.8)
                submitted = api.list_orders(symbol="ftusdt", states="submitted")
                if submitted != None and submitted["status"] == 0:
                    for CurOrder in submitted["data"]:
                        OrderList[CurOrder["id"]] = CurOrder
                        TempList[CurOrder["id"]] = CurOrder
                else:
                    time.sleep(1)
                    continue
                for (key, CurOrder) in OldList.items():
                    if key not in TempList:
                        del OrderList[key]
                with OrderLock:
                    Actions = OrderActions.copy()
                OrderSend=OrderList.copy()
                for cur in Actions:
                    cur(OrderSend)
                time.sleep(1)
        except:
            with OrderLock:
                OrderThread = None
                print("Order线程异常结束")
                StartOrderThread()


def StopOrderThread():
    global OrderThread,OrderLock
    with OrderLock:
        if OrderThread != None:
            OrderThread._stop()
            OrderThread = None


def StartOrderThread():
    global OrderThread,OrderLock
    with OrderLock:
        StopOrderThread()
        OrderThread = OrderThreadClass()
        OrderThread.start()

def StopBalanceThread():
    global BalanceThread,BalanceLock
    with BalanceLock:
        if BalanceThread != None:
            BalanceThread._stop()
            BalanceThread = None


def StartBalanceThread():
    global BalanceThread,BalanceLock
    with BalanceLock:
        StopBalanceThread()
        BalanceThread = BalanceThreadClass()
        BalanceThread.start()

class FCoinClass():
    def __init__(self):
        StartBalanceThread()
        StartOrderThread()

    def DoBuy(self,stock,price,qty):
        global api
        Result = api.buy(stock, price, qty)
        if Result != None and Result["status"] == 0:
            print(Result)


    def DoSell(self,stock,price,qty):
        global api
        Result = api.sell(stock, price, qty)
        if Result != None and Result["status"] == 0:
            print(Result)

    def AddBalanceAction(self,action):
        global BalanceLock, BalanceActions
        with BalanceLock:
            BalanceActions.add(action)

    def RemoveBalanceAction(self,action):
        global BalanceLock, BalanceActions
        with BalanceLock:
            try:
                BalanceActions.remove(action)
            except:
                print("RemoveBalanceActionError")

    def AddOrderAction(self,action):
        global OrderLock, OrderActions
        with OrderLock:
            OrderActions.add(action)

    def RemoveOrderAction(self,action):
        global OrderLock, OrderActions
        with OrderLock:
            try:
                OrderActions.remove(action)
            except:
                print("RemoveBalanceActionError")

