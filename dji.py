# -*- coding: utf-8 -*-
import wx
import urllib
import json

from custom_dialogs import ConfigureData


class StockFrame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, size=(500,600))

        self.CreateStatusBar()

        menuBar = wx.MenuBar()

        filemenu= wx.Menu()
        menuBar.Append(filemenu,"&File")
        
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," About")
        filemenu.AppendSeparator()

        menuQuit = filemenu.Append(wx.ID_EXIT,"Q&uit"," Terminate the program")
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnQuit, menuQuit)
        self.SetMenuBar(menuBar)

        panel = wx.Panel(self)

        #原本是一个显示股票代码的窗口,感觉比较鸡肋,做了些修改
        codeSizer = wx.BoxSizer(wx.HORIZONTAL)
        labelText = wx.StaticText(panel, label="Real-Time Stock Charting")
        codeSizer.Add(labelText, 0, wx.ALIGN_BOTTOM)
        codeSizer.Add((10, 10))
        # addressText = wx.TextCtrl(panel, value='IBM')
        # addressText.SetSize(addressText.GetBestFittingSize())
        # codeSizer.Add(addressText)
        
        self.list = wx.ListCtrl(panel, wx.NewId(), style=wx.LC_REPORT)
        self.list.InsertColumn(0,"Stock Code")
        self.list.InsertColumn(1,"Name")
        self.list.InsertColumn(2,"Price")  

        pos = self.list.InsertStringItem(0,"--")
        self.list.SetStringItem(pos,1,"loading...")
        self.list.SetStringItem(pos,2,"--")  
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnClick, self.list)
        
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(codeSizer, 0, wx.ALL, 10)
        vsizer.Add(self.list, -1, wx.ALL | wx.EXPAND, 10)
        #panel.SetSizer(self.sizer)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add((10, 10))
        buttonQuit = wx.Button(panel, -1, "Quit")
        self.Bind(wx.EVT_BUTTON, self.OnQuit, buttonQuit)
        buttonQuit.SetDefault()
        hsizer.Add(buttonQuit, 1)

        buttonRefresh = wx.Button(panel, -1, "Refresh")
        self.Bind(wx.EVT_BUTTON, self.OnRefresh, buttonRefresh)
        hsizer.Add(buttonRefresh, 1)
        
        vsizer.Add(hsizer, 0, wx.ALIGN_BOTTOM)
       

        panel.SetSizerAndFit(vsizer)        
        panel.Layout()        
        
        
        '''frameSizer = wx.BoxSizer(wx.VERTICAL)
        frameSizer.Add(panel)
        self.SetSizerAndFit(frameSizer)
        self.Layout()
        self.Fit()'''

    #遍历获取的股票信息，呈现出来
    def setData(self,data):
        self.list.ClearAll()
        self.list.InsertColumn(0,"Code")
        self.list.InsertColumn(1,"Name")
        self.list.InsertColumn(2,"Price")  

        pos = 0
        for row in data:            
            pos = self.list.InsertStringItem(pos+1, row[0])
            # self.list.SetStringItem(pos, 1, row[1])
            self.list.SetStringItem(pos, 1, row[1].replace("&amp;", "&"))
            self.list.SetColumnWidth(1, -1)
            self.list.SetStringItem(pos, 2, row[2])
            if (pos % 2 == 0):
                    # Get the item at a specific index:
                    #item = self.list.GetItem(pos)
                self.list.SetItemBackgroundColour(pos, (134, 225, 249))
                # Set new look and feel back to the list
                #self.list.SetItem(item)
        self.FitInside()
        pass
        
    def GetAllSelected(self):
        selection = []

        # start at -1 to get the first selected item
        current = -1
        while True:
            next = self.GetNextSelected(current)
            if next == -1:
                return selection

            selection.append(self.list.GetItemText(next))
            current = next

    #选取行中的第一个元素时，接着选中行中所有后续元素
    def GetNextSelected(self, current):
        return self.list.GetNextItem(current,
                                wx.LIST_NEXT_ALL,
                                wx.LIST_STATE_SELECTED)

    def OnClick(self, event):
        codes = self.GetAllSelected()
        print "code in DJI", codes
        #将股票代码传递给custom_dialogs.py
        ConfigureData(codes)
        
    def OnAbout(self, event):
        dlg = wx.MessageDialog( self, "A Real-Time Stock Charting Program", "About this program", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnQuit(self, event):
        self.Close()
        self.Destroy()
        
    def OnRefresh(self, event):
        self.getstatics()

    def getstatics(self):
        url = urllib.urlopen('http://query1.finance.yahoo.com/v7/finance/quote?formatted=true&crumb=azVqAvrYffI&lang=en-US&region=US&symbols=DD%2CAAPL%2CCSCO%2CCVX%2CVZ%2CJPM%2CJNJ%2CMRK%2CPFE%2CUNH%2CMSFT%2CIBM%2CV%2CUTX%2CTRV%2CGE%2CKO%2CNKE%2CGS%2CMMM%2CDIS%2CMCD%2CINTC%2CCAT%2CPG%2CXOM%2CAXP%2CHD%2CBA%2CWMT&fields=longName%2CregularMarketPrice%2CregularMarketChange%2CregularMarketChangePercent&corsDomain=finance.yahoo.com')
        # print str

        resp = json.loads(url.read().decode('utf-8'))

        infolist = []
        if resp:
            for stock in resp['quoteResponse']['result']:
                # print(stock['symbol'], stock['longName'], stock['regularMarketPrice']['fmt'])
                infolist.append([stock['symbol'],stock['longName'],stock['regularMarketPrice']['fmt']])
            top.setData(infolist)
            # print infolist
        else:  
            wx.MessageBox('Download failed.', 'Message',  wx.OK | wx.ICON_INFORMATION)

app = wx.App(False)

top = StockFrame("Companies in the Dow Jones Industrial Average")
top.Show(True)
top.getstatics()
# def getstatics(self):
# url = urllib.urlopen('http://query1.finance.yahoo.com/v7/finance/quote?formatted=true&crumb=azVqAvrYffI&lang=en-US&region=US&symbols=DD%2CAAPL%2CCSCO%2CCVX%2CVZ%2CJPM%2CJNJ%2CMRK%2CPFE%2CUNH%2CMSFT%2CIBM%2CV%2CUTX%2CTRV%2CGE%2CKO%2CNKE%2CGS%2CMMM%2CDIS%2CMCD%2CINTC%2CCAT%2CPG%2CXOM%2CAXP%2CHD%2CBA%2CWMT&fields=longName%2CregularMarketPrice%2CregularMarketChange%2CregularMarketChangePercent&corsDomain=finance.yahoo.com')
# # print str

# resp = json.loads(url.read().decode('utf-8'))

# infolist = []
# if resp:
#     for stock in resp['quoteResponse']['result']:
#         # print(stock['symbol'], stock['longName'], stock['regularMarketPrice']['fmt'])
#         infolist.append([stock['symbol'],stock['longName'],stock['regularMarketPrice']['fmt']])
#     top.setData(infolist)
#     # print infolist
# else:  
#     wx.MessageBox('Download failed.', 'Message',  wx.OK | wx.ICON_INFORMATION)

app.MainLoop()


