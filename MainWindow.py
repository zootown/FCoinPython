# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import time
import L2Window
import threading
import FCoinWs

###########################################################################
## Class MainWindow
###########################################################################

class MainWindow(wx.Frame):

    def __init__(self, parent=None):
        self.L2Lock=threading.RLock()
        self.L2List={}
        #全在主线程处理，暂不lock
        self.WsList={}
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(739, 436), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        gSizer10 = wx.GridSizer(2, 0, 0, 0)

        gSizer11 = wx.GridSizer(0, 2, 0, 0)

        self.buttonL2 = wx.Button(self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer11.Add(self.buttonL2, 0, wx.ALL, 5)

        gSizer10.Add(gSizer11, 1, wx.EXPAND, 5)

        gSizer12 = wx.GridSizer(0, 2, 0, 0)

        gSizer10.Add(gSizer12, 1, wx.EXPAND, 5)

        self.SetSizer(gSizer10)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.buttonL2.Bind(wx.EVT_BUTTON, self.buttonL2OnButtonClick)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def buttonL2OnButtonClick(self, event):
        self.AddL2Window("ft", "usdt")
        event.Skip()

    def RemoveL2Window(self,key):
        with self.L2Lock:
            try:
                del self.L2List[key]
            except:
                pass

    def AddL2Window(self,s1,s2):
        with self.L2Lock:
            key = (s1 + s2).lower()
            if key not in self.L2List:
                CurStockFame = L2Window.L2Form(s1, s2, self)
                CurStockFame.Show()
                self.L2List[key] = CurStockFame
                CurStockFame.FrameInit()
                if key not in self.WsList:
                    ws=FCoinWs.FCoinWsClass(key)
                    self.WsList[key]=ws
                    ws.AddDepthAction(CurStockFame.RefreshQuote)
            else:
                pass

if __name__ == "__main__":
    BaseTimeT = int(time.time() * 1000)
    app = wx.App()
    mainwin = MainWindow()
    mainwin.Show()
    app.MainLoop()