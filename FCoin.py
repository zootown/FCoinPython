import  fcoin
import threading
import configparser


cf = configparser.ConfigParser()
cf.read("fcoin.ini")
key = cf.get("Key", "Public")
secret = cf.get("Key", "Secret")

class FCoinClass():
    def __init__(self):
        self.api = fcoin.authorize(key, secret)

    def DoBuy(self,stock,price,qty):
        Result = self.api.buy(stock, price, qty)
        if Result != None and Result["status"] == 0:
            print(Result)


    def DoSell(self,stock,price,qty):
        global api
        Result = api.sell(stock, price, qty)
        if Result != None and Result["status"] == 0:
            print(Result)
        self.SetSellDisable()






