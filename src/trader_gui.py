#!/usr/bin/env python

import os
import wx

import yapsy.PluginManager

import trader
import plugins


class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        self.CreateStatusBar()
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        item = menu.Append(wx.ID_OPEN, '&Open\tCtrl+O',
                           'Open a market data file')
        self.Bind(wx.EVT_MENU, self.OnOpen, item)
        menu.AppendSeparator()
        item = menu.Append(wx.ID_ANY, '&Export',
                           'Save outputted trades')
        self.Bind(wx.EVT_MENU, self.OnExport, item)
        menu.AppendSeparator()
        item = menu.Append(wx.ID_CLOSE, '&Close\tCtrl+W',
                           'Close the current market data file')
        item = menu.Append(wx.ID_EXIT, 'E&xit\tCtrl+Q',
                           'Terminate the program')
        self.Bind(wx.EVT_MENU, self.OnExit, item)
        menuBar.Append(menu, '&File')
        menu = wx.Menu()
        item = menu.Append(wx.ID_ANY, '&Initialize',
                           'Initialize order book')
        self.Bind(wx.EVT_MENU, self.OnInitialize, item)
        item = menu.Append(wx.ID_ANY, '&Run',
                           'Run trial')
        self.Bind(wx.EVT_MENU, self.OnRun, item)
        menuBar.Append(menu, '&Tools')
        menu = wx.Menu()
        item = menu.Append(wx.ID_ABOUT, '&About',
                           'Information about this program')
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        menuBar.Append(menu, '&Help')
        self.SetMenuBar(menuBar)

    def OnOpen(self, e):
        wildcard = 'CSV files (*.csv)|*.csv|Text files (*.txt)|*.txt|' \
                   'All files (*.*)|*.*'
        dlg = wx.FileDialog(self, wildcard=wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            pass
        dlg.Destroy()

    def OnExport(self, e):
        raise NotImplementedError

    def OnClose(self, e):
        raise NotImplementedError

    def OnInitialize(self, e):
        raise NotImplementedError

    def OnRun(self, e):
        raise NotImplementedError

    def OnExit(self, e):
        self.Close(True)

    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, 'Algorithmic Trading System',
                               'Algorithmic Trading System', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()


def main():
    app = wx.App(False)
    MainFrame(None, 'Algorithmic Trading System').Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
