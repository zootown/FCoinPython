import wx
import wx.xrc
import wx.dataview
import fcoin
import threading
import time
import json
import datetime


class L2Form(wx.Frame):
    def __init__(self, stock1, stock2, parent=None):
        self.parent=parent
        self.OrderList = {}
        self.depth = None
        self.QuoteThread = None
        self.RefreshThread = None
        self.OrderThread = None
        self.Stock1 = stock1
        self.Stock2 = stock2
        self.StockText = stock1.upper() + "/" + stock2.upper()
        self.RequestStockText = stock1.lower() + stock2.lower()
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(593, 612), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(12, 70, 90, 90, False, "宋体"))

        gSizer8 = wx.GridSizer(0, 2, 0, 0)

        fgSizer69 = wx.FlexGridSizer(2, 0, 0, 0)
        fgSizer69.SetFlexibleDirection(wx.BOTH)
        fgSizer69.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.QuoteList = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(280, 450), wx.LC_REPORT)
        self.QuoteList.SetFont(wx.Font(12, 70, 90, 90, False, "宋体"))
        self.QuoteList.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.QuoteList.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))

        fgSizer69.Add(self.QuoteList, 0, wx.ALL, 5)

        self.TickView = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(280, 450), wx.LC_REPORT)
        self.TickView.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.TickView.SetBackgroundColour(wx.Colour(64, 64, 64))

        fgSizer69.Add(self.TickView, 0, wx.ALL, 5)

        gSizer8.Add(fgSizer69, 1, wx.EXPAND, 5)

        gSizer10 = wx.GridSizer(2, 0, 0, 0)

        self.OrderView = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(280, 280), wx.LC_REPORT)
        self.OrderView.SetFont(wx.Font(10, 70, 90, 90, False, "宋体"))
        self.OrderView.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.OrderView.SetBackgroundColour(wx.Colour(64, 64, 64))

        gSizer10.Add(self.OrderView, 0, wx.ALL, 5)

        gSizer4 = wx.GridSizer(2, 0, 0, 0)

        gSizer5 = wx.GridSizer(2, 0, 0, 0)

        gSizer7 = wx.GridSizer(2, 2, 0, 0)

        fgSizer1 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Stock2Name = wx.StaticText(self, wx.ID_ANY, u"货币:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Stock2Name.Wrap(-1)
        self.Stock2Name.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_CAPTIONTEXT))

        fgSizer1.Add(self.Stock2Name, 0, wx.ALL, 5)

        self.Stock2Balance = wx.StaticText(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Stock2Balance.Wrap(-1)
        self.Stock2Balance.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        fgSizer1.Add(self.Stock2Balance, 0, wx.ALL, 5)

        gSizer7.Add(fgSizer1, 1, wx.EXPAND, 5)

        gbSizer2 = wx.GridBagSizer(0, 0)
        gbSizer2.SetFlexibleDirection(wx.BOTH)
        gbSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Stock1Name = wx.StaticText(self, wx.ID_ANY, u"货币:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Stock1Name.Wrap(-1)
        self.Stock1Name.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))

        gbSizer2.Add(self.Stock1Name, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.Stock1Balance = wx.StaticText(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Stock1Balance.Wrap(-1)
        self.Stock1Balance.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        gbSizer2.Add(self.Stock1Balance, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        gSizer7.Add(gbSizer2, 1, wx.EXPAND, 5)

        fgSizer2 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText5 = wx.StaticText(self, wx.ID_ANY, u"可用:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)
        fgSizer2.Add(self.m_staticText5, 0, wx.ALL, 5)

        self.Stock2CanUse = wx.StaticText(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Stock2CanUse.Wrap(-1)
        self.Stock2CanUse.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        fgSizer2.Add(self.Stock2CanUse, 0, wx.ALL, 5)

        gSizer7.Add(fgSizer2, 1, wx.EXPAND, 5)

        fgSizer4 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer4.SetFlexibleDirection(wx.BOTH)
        fgSizer4.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText7 = wx.StaticText(self, wx.ID_ANY, u"可用:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText7.Wrap(-1)
        fgSizer4.Add(self.m_staticText7, 0, wx.ALL, 5)

        self.Stock1CanUse = wx.StaticText(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Stock1CanUse.Wrap(-1)
        self.Stock1CanUse.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        fgSizer4.Add(self.Stock1CanUse, 0, wx.ALL, 5)

        gSizer7.Add(fgSizer4, 1, wx.EXPAND, 5)

        gSizer5.Add(gSizer7, 1, wx.EXPAND, 5)

        gSizer81 = wx.GridSizer(2, 2, 0, 0)

        fgSizer41 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer41.SetFlexibleDirection(wx.BOTH)
        fgSizer41.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText9 = wx.StaticText(self, wx.ID_ANY, u"价格:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText9.Wrap(-1)
        fgSizer41.Add(self.m_staticText9, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.BuyPrice = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size(90, -1), 0)
        fgSizer41.Add(self.BuyPrice, 0, wx.ALL, 5)

        gSizer81.Add(fgSizer41, 1, wx.EXPAND, 5)

        fgSizer5 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer5.SetFlexibleDirection(wx.BOTH)
        fgSizer5.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText10 = wx.StaticText(self, wx.ID_ANY, u"价格:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText10.Wrap(-1)
        fgSizer5.Add(self.m_staticText10, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SellPrice = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size(90, -1), 0)
        fgSizer5.Add(self.SellPrice, 0, wx.ALL, 5)

        gSizer81.Add(fgSizer5, 1, wx.EXPAND, 5)

        fgSizer6 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer6.SetFlexibleDirection(wx.BOTH)
        fgSizer6.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText11 = wx.StaticText(self, wx.ID_ANY, u"数量:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText11.Wrap(-1)
        fgSizer6.Add(self.m_staticText11, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.BuyQty = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size(90, -1), 0)
        fgSizer6.Add(self.BuyQty, 0, wx.ALL, 5)

        gSizer81.Add(fgSizer6, 1, wx.EXPAND, 5)

        fgSizer7 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer7.SetFlexibleDirection(wx.BOTH)
        fgSizer7.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText12 = wx.StaticText(self, wx.ID_ANY, u"数量:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText12.Wrap(-1)
        fgSizer7.Add(self.m_staticText12, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SellQty = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size(90, -1), 0)
        fgSizer7.Add(self.SellQty, 0, wx.ALL, 5)

        gSizer81.Add(fgSizer7, 1, wx.EXPAND, 5)

        gSizer5.Add(gSizer81, 1, wx.EXPAND, 5)

        gSizer4.Add(gSizer5, 1, wx.EXPAND, 5)

        gSizer6 = wx.GridSizer(2, 0, 0, 0)

        gSizer101 = wx.GridSizer(2, 2, 0, 0)

        fgSizer8 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer8.SetFlexibleDirection(wx.BOTH)
        fgSizer8.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        gSizer101.Add(fgSizer8, 1, wx.EXPAND, 5)

        fgSizer9 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer9.SetFlexibleDirection(wx.BOTH)
        fgSizer9.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        gSizer101.Add(fgSizer9, 1, wx.EXPAND, 5)

        self.BuyButton = wx.Button(self, wx.ID_ANY, u"买入", wx.DefaultPosition, wx.Size(120, -1), 0)
        self.BuyButton.SetForegroundColour(wx.Colour(255, 255, 255))
        self.BuyButton.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))
        self.BuyButton.Enable(False)

        gSizer101.Add(self.BuyButton, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SellButton = wx.Button(self, wx.ID_ANY, u"卖出", wx.DefaultPosition, wx.Size(120, -1), 0)
        self.SellButton.SetForegroundColour(wx.Colour(255, 255, 255))
        self.SellButton.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))
        self.SellButton.Enable(False)

        gSizer101.Add(self.SellButton, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        gSizer6.Add(gSizer101, 1, wx.EXPAND, 5)

        gSizer11 = wx.GridSizer(2, 2, 0, 0)

        fgSizer11 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer11.SetFlexibleDirection(wx.BOTH)
        fgSizer11.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText13 = wx.StaticText(self, wx.ID_ANY, u"默认买:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText13.Wrap(-1)
        fgSizer11.Add(self.m_staticText13, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.DefaultBuy = wx.SpinCtrl(self, wx.ID_ANY, u"8000", wx.DefaultPosition, wx.Size(70, -1), wx.SP_ARROW_KEYS,
                                      0, 10, 0)
        fgSizer11.Add(self.DefaultBuy, 0, wx.ALL, 5)

        gSizer11.Add(fgSizer11, 1, wx.EXPAND, 5)

        fgSizer12 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer12.SetFlexibleDirection(wx.BOTH)
        fgSizer12.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText14 = wx.StaticText(self, wx.ID_ANY, u"默认卖:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText14.Wrap(-1)
        fgSizer12.Add(self.m_staticText14, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.DefaultSell = wx.SpinCtrl(self, wx.ID_ANY, u"7992", wx.DefaultPosition, wx.Size(70, -1), wx.SP_ARROW_KEYS,
                                       0, 10, 0)
        fgSizer12.Add(self.DefaultSell, 0, wx.ALL, 5)

        gSizer11.Add(fgSizer12, 1, wx.EXPAND, 5)

        fgSizer13 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer13.SetFlexibleDirection(wx.BOTH)
        fgSizer13.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.ButtonRefresh = wx.Button(self, wx.ID_ANY, u"刷新", wx.DefaultPosition, wx.Size(120, -1), 0)
        self.ButtonRefresh.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOTEXT))
        self.ButtonRefresh.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        fgSizer13.Add(self.ButtonRefresh, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        gSizer11.Add(fgSizer13, 1, wx.EXPAND, 5)

        fgSizer14 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer14.SetFlexibleDirection(wx.BOTH)
        fgSizer14.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        gSizer11.Add(fgSizer14, 1, wx.EXPAND, 5)

        gSizer6.Add(gSizer11, 1, wx.EXPAND, 5)

        gSizer4.Add(gSizer6, 1, wx.EXPAND, 5)

        gSizer10.Add(gSizer4, 1, wx.EXPAND, 5)

        gSizer8.Add(gSizer10, 1, wx.EXPAND, 5)

        self.SetSizer(gSizer8)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_CLOSE, self.L2FormOnClose)
        self.Bind(wx.EVT_KEY_UP, self.MyFrame2OnKeyUp)
        self.QuoteList.Bind(wx.EVT_KEY_UP, self.QuoteListOnKeyUp)
        self.OrderView.Bind(wx.EVT_KEY_UP, self.OrderListOnKeyUp)
        self.TickView.Bind(wx.EVT_KEY_UP, self.TickListOnKeyUp)
        self.BuyPrice.Bind(wx.EVT_KEY_UP, self.BuyPriceOnKeyUp)
        self.SellPrice.Bind(wx.EVT_KEY_UP, self.SellPriceOnKeyUp)
        self.BuyQty.Bind(wx.EVT_KEY_UP, self.BuyQtyOnKeyUp)
        self.SellQty.Bind(wx.EVT_KEY_UP, self.SellQtyOnKeyUp)
        self.BuyButton.Bind(wx.EVT_BUTTON, self.BuyButtonOnButtonClick)
        self.SellButton.Bind(wx.EVT_BUTTON, self.SellButtonOnButtonClick)
        self.ButtonRefresh.Bind(wx.EVT_BUTTON, self.ButtonRefreshOnButtonClick)

    def L2FormOnClose(self, event):
        self.parent.RemoveL2Window(self.RequestStockText)
        event.Skip()

    def DealOtherKey(self, key):
        if key == wx.WXK_F4:
            if self.depth != None:
                self.BuyPrice.Value = str(self.depth["data"]["asks"][0])
                self.BuyQty.Value = str(self.DefaultBuy.Value)
                self.SetBuyEnable()
                self.SetSellDisable()
        elif key == wx.WXK_F3:
            if self.depth != None:
                self.SellPrice.Value = str(self.depth["data"]["bids"][0])
                self.SellQty.Value = str(self.DefaultSell.Value)
                self.SetSellEnable()
                self.SetBuyDisable()
        elif key == wx.WXK_F6:
            if self.depth != None:
                self.BuyPrice.Value = str(self.depth["data"]["bids"][0])
                self.BuyQty.Value = str(self.DefaultBuy.Value)
                self.SetBuyEnable()
                self.SetSellDisable()
        elif key == wx.WXK_F5:
            if self.depth != None:
                self.SellPrice.Value = str(self.depth["data"]["asks"][0])
                self.SellQty.Value = str(self.DefaultSell.Value)
                self.SetSellEnable()
                self.SetBuyDisable()
        elif key == wx.WXK_ESCAPE:
            self.CancelLast()
        elif key == wx.WXK_RETURN:
            if self.BuyButton.Enabled:
                self.DoBuy()
            elif self.SellButton.Enabled:
                self.DoSell()
        if key == wx.WXK_UP:
            if self.BuyButton.Enabled:
                box = self.BuyPrice
            elif self.SellButton.Enabled:
                box = self.SellPrice
            else:
                return
            Price = round(float(box.Value) + 0.0002, 6)
            box.Value = str(Price)
        elif key == wx.WXK_DOWN:
            if self.BuyButton.Enabled:
                box = self.BuyPrice
            elif self.SellButton.Enabled:
                box = self.SellPrice
            else:
                return
            Price = round(float(box.Value) - 0.0002, 6)
            box.Value = str(Price)
        if key == wx.WXK_RIGHT:
            if self.BuyButton.Enabled:
                box = self.BuyQty
            elif self.SellButton.Enabled:
                box = self.SellQty
            else:
                return
            Qty = float(box.Value)
            Qty += 100
            box.Value = str(Qty)
        elif key == wx.WXK_LEFT:
            if self.BuyButton.Enabled:
                box = self.BuyQty
            elif self.SellButton.Enabled:
                box = self.SellQty
            else:
                return
            Qty = float(box.Value)
            Qty -= 100
            box.Value = str(Qty)

    def MyFrame2OnKeyUp(self, event):
        self.DealOtherKey(event.KeyCode)
        event.Skip()

    def QuoteListOnKeyUp(self, event):
        self.DealOtherKey(event.KeyCode)
        event.Skip()

    def OrderListOnKeyUp(self, event):
        self.DealOtherKey(event.KeyCode)
        event.Skip()

    def TickListOnKeyUp(self, event):
        self.DealOtherKey(event.KeyCode)
        event.Skip()

    def BuyPriceOnKeyUp(self, event):
        self.DealOtherKey(event.KeyCode)
        event.Skip()

    def SellPriceOnKeyUp(self, event):
        self.DealOtherKey(event.KeyCode)
        event.Skip()

    def BuyQtyOnKeyUp(self, event):
        self.DealOtherKey(event.KeyCode)
        event.Skip()

    def SellQtyOnKeyUp(self, event):
        self.DealOtherKey(event.KeyCode)
        event.Skip()

    def BuyButtonOnButtonClick(self, event):
        self.DoBuy()
        event.Skip()

    def SellButtonOnButtonClick(self, event):
        self.DoSell()
        event.Skip()

    def ButtonRefreshOnButtonClick(self, event):
        self.DoRefresh()

    def DoRefresh(self):
        # Balance
        global api, Balances
        Result = api.get_balance()
        if Result != None and "data" in Result:
            for CurStock in Result["data"]:
                Balances[CurStock["currency"]] = [round(float(CurStock["balance"]), 4),
                                                  round(float(CurStock["available"]), 4)]
            self.ShowBalance()

        # Order
        TempList = {}
        OldList = self.OrderList.copy()
        partial_filled = api.list_orders(symbol="ftusdt", states="partial_filled")
        if partial_filled != None and partial_filled["status"] == 0:
            for CurOrder in partial_filled["data"]:
                self.OrderList[CurOrder["id"]] = CurOrder
                TempList[CurOrder["id"]] = CurOrder
        submitted = api.list_orders(symbol="ftusdt", states="submitted")
        if submitted != None and submitted["status"] == 0:
            for CurOrder in submitted["data"]:
                self.OrderList[CurOrder["id"]] = CurOrder
                TempList[CurOrder["id"]] = CurOrder
        for (key, CurOrder) in OldList.items():
            if key not in TempList:
                del self.OrderList[key]
        self.RefreshOrder(self.OrderList.copy())

    def SetBuyEnable(self):
        self.BuyButton.SetBackgroundColour(ButtonBuyColor)
        self.BuyButton.Enable(True)

    def SetBuyDisable(self):
        self.BuyButton.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))
        self.BuyButton.Enable(False)

    def SetSellEnable(self):
        self.SellButton.SetBackgroundColour(ButtonSellColor)
        self.SellButton.Enable(True)

    def SetSellDisable(self):
        self.SellButton.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))
        self.SellButton.Enable(False)

    def DoBuy(self):
        global api
        Result = api.buy(self.RequestStockText, self.BuyPrice.Value, self.BuyQty.Value)
        if Result != None and Result["status"] == 0:
            print(Result)
        self.SetBuyDisable()
        print(Result)

    def DoSell(self):
        global api
        Result = api.sell(self.RequestStockText, self.SellPrice.Value, self.SellQty.Value)
        if Result != None and Result["status"] == 0:
            print(Result)
        self.SetSellDisable()
        print(Result)

    def CancelOrder(self, id):
        global api
        Result = api.cancel_order(id)
        if Result != None and Result["status"] == 0:
            print(Result)

    def CancelLast(self):
        Orders = self.OrderList.copy()
        sorted(Orders, reverse=False)
        for (key, CurOrder) in Orders.items():
            self.CancelOrder(key)
            break;

    def SetItemText(self, CurOrder, ItemIndex):
        self.OrderView.SetItem(ItemIndex, 1, str(round(float(CurOrder["price"]), 6)))
        self.OrderView.SetItem(ItemIndex, 2, str(round(float(CurOrder["amount"]), 0)))
        self.OrderView.SetItem(ItemIndex, 3, str(round(float(CurOrder["filled_amount"]), 0)))

    def RefreshOrder(self, TempOrders):
        DelList = {}
        for Index in range(0, self.OrderView.ItemCount):
            HadItem = False
            ItemData = self.OrderView.GetItemData(Index)
            for (key, CurOrder) in TempOrders.items():
                if CurOrder["created_at"] - BaseTimeT == ItemData:
                    HadItem = True;
                    break;
            if not HadItem:
                DelList[Index] = 0
        sorted(DelList, reverse=False)
        for CurIndex in DelList:
            self.OrderView.DeleteItem(CurIndex)
        for CurOrder in TempOrders.values():
            ItemIndex = -1
            OrderRealTime = CurOrder["created_at"]
            OrderTime = CurOrder["created_at"] - BaseTimeT
            for Index in range(0, self.OrderView.ItemCount):
                if self.OrderView.GetItemData(Index) == OrderTime:
                    ItemIndex = Index
                    break
            if ItemIndex >= 0:
                self.SetItemText(CurOrder, ItemIndex)
            else:
                ItemIndex = self.OrderView.InsertItem(0, datetime.datetime.fromtimestamp(OrderRealTime / 1000).strftime(
                    "%H:%M:%S"));
                self.OrderView.SetItemData(ItemIndex, OrderTime);
                t1 = self.OrderView.GetItem(ItemIndex);
                d1 = self.OrderView.GetItemData(ItemIndex);
                self.SetItemText(CurOrder, ItemIndex)

    def ShowBalance(self):
        global Balances
        if self.Stock1 in Balances:
            self.Stock1Balance.SetLabelText(str(Balances[self.Stock1][0]))
            self.Stock1CanUse.SetLabelText(str(Balances[self.Stock1][1]))
        if self.Stock2 in Balances:
            self.Stock2Balance.SetLabelText(str(Balances[self.Stock2][0]))
            self.Stock2CanUse.SetLabelText(str(Balances[self.Stock2][1]))

    def RefreshQuote(self, quote):
        asks = quote["data"]["asks"]
        if len(asks) >= 20:
            Total = 0
            for i in range(10):
                self.QuoteList.SetItemText(9 - i, str(asks[i * 2]));
                size = int(asks[i * 2 + 1])
                Total += size
                self.QuoteList.SetItem(9 - i, 1, str(size));
                self.QuoteList.SetItem(9 - i, 2, str(Total));
        bids = quote["data"]["bids"]
        if len(bids) >= 20:
            Total = 0
            for i in range(10):
                self.QuoteList.SetItemText(11 + i, str(bids[i * 2]));
                size = int(bids[i * 2 + 1])
                Total += size
                self.QuoteList.SetItem(11 + i, 1, str(size));
                self.QuoteList.SetItem(11 + i, 2, str(Total));

    def FrameInit(self):
        self.SetTitle(self.StockText)
        self.QuoteList.InsertColumn(0, "价格")
        self.QuoteList.InsertColumn(1, "数量")
        self.QuoteList.InsertColumn(2, "累积")
        self.OrderView.InsertColumn(0, "时间")
        self.OrderView.SetColumnWidth(1, 70)
        self.OrderView.InsertColumn(1, "价格")
        self.OrderView.SetColumnWidth(1, 60)
        self.OrderView.InsertColumn(2, "数量")
        self.OrderView.SetColumnWidth(2, 60)
        self.OrderView.InsertColumn(3, "成交")
        self.OrderView.SetColumnWidth(3, 60)
        self.Stock1Name.SetLabelText(self.Stock1.upper() + ":")
        self.Stock2Name.SetLabelText(self.Stock2.upper() + ":")
        self.DefaultBuy.SetMax(99999999)
        self.DefaultSell.SetMax(99999999)
        self.SetBuyDisable()
        self.SetSellDisable()
        for i in range(10):
            ItemIndex = self.QuoteList.InsertItem(i, "0")
            self.QuoteList.SetItemTextColour(ItemIndex, wx.Colour(255, 0, 0))
        ItemIndex = self.QuoteList.InsertItem(10, "0")
        self.QuoteList.SetItemTextColour(ItemIndex, wx.Colour(255, 255, 255))
        for i in range(11, 21):
            ItemIndex = self.QuoteList.InsertItem(i, "0")
            self.QuoteList.SetItemTextColour(ItemIndex, wx.Colour(0, 255, 0))

    def __del__(self):
        pass

if __name__ == "__main__":
    ButtonBuyColor = wx.Colour(6, 176, 124)
    ButtonSellColor = wx.Colour(255, 83, 83)
    BaseTimeT = int(time.time() * 1000)
    app = wx.App()
    CurStockFame = L2Form("ft", "usdt")
    CurStockFame.Show()
    CurStockFame.FrameInit()
    app.MainLoop()

