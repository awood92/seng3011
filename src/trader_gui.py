#!/usr/bin/env python

import os
import wx

import yapsy.PluginManager

import trader
import plugins


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs)
        self.InitUI()

    def InitUI(self):
        self._status_bar = self.CreateStatusBar()
        self._tool_bar = self.CreateToolBar()
        menu_bar = wx.MenuBar()
        menu = wx.Menu()
        item = menu.Append(wx.ID_OPEN, '&Open\tCtrl+O',
                           'Open a market data file')
        self.Bind(wx.EVT_MENU, self.OnOpen, item)
        item = menu.Append(wx.ID_ANY, '&Export',
                           'Save outputted trades')
        self.Bind(wx.EVT_MENU, self.OnExport, item)
        menu.AppendSeparator()
        item = menu.Append(wx.ID_CLOSE, '&Close\tCtrl+W',
                           'Close the current market data file')
        item = menu.Append(wx.ID_EXIT, 'E&xit\tCtrl+Q',
                           'Terminate the program')
        self.Bind(wx.EVT_MENU, self.OnExit, item)
        menu_bar.Append(menu, '&File')
        menu = wx.Menu()
        self._item_status_bar = menu.Append(wx.ID_ANY, 'Show &Statusbar',
                                            'Toggle visibility of statusbar',
                                            wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self._item_status_bar)
        menu.Check(self._item_status_bar.GetId(), True)
        self._item_tool_bar = menu.Append(wx.ID_ANY, 'Show &Toolbar',
                                          'Toggle visibility of toolbar',
                                          wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.ToggleToolBar, self._item_tool_bar)
        menu.Check(self._item_tool_bar.GetId(), True)
        menu_bar.Append(menu, '&View')
        menu = wx.Menu()
        item = menu.Append(wx.ID_ANY, '&Run',
                           'Run trial')
        self.Bind(wx.EVT_MENU, self.OnRun, item)
        menu_bar.Append(menu, '&Tools')
        menu = wx.Menu()
        item = menu.Append(wx.ID_ABOUT, '&About',
                           'Information about this program')
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        menu_bar.Append(menu, '&Help')
        self.SetMenuBar(menu_bar)
        icon = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN)
        tool = self._tool_bar.AddLabelTool(wx.ID_OPEN, 'Open', icon)
        self.Bind(wx.EVT_TOOL, self.OnOpen, tool)
        icon = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS)
        tool = self._tool_bar.AddLabelTool(wx.ID_ANY, 'Export', icon)
        self.Bind(wx.EVT_TOOL, self.OnExport, tool)
        self._tool_bar.AddSeparator()
        icon = wx.ArtProvider.GetBitmap(wx.ART_CROSS_MARK)
        tool = self._tool_bar.AddLabelTool(wx.ID_CLOSE, 'Close', icon)
        self.Bind(wx.EVT_TOOL, self.OnClose, tool)
        self._tool_bar.AddSeparator()
        icon = wx.Bitmap('resources/run.png')
        tool = self._tool_bar.AddLabelTool(wx.ID_ANY, 'Run', icon)
        self.Bind(wx.EVT_TOOL, self.OnRun, tool)

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

    def OnExit(self, e):
        self.Close(True)

    def ToggleStatusBar(self, e):
        if self._item_status_bar.IsChecked():
            self._status_bar.Show()
        else:
            self._status_bar.Hide()

    def ToggleToolBar(self, e):
        if self._item_tool_bar.IsChecked():
            self._tool_bar.Show()
        else:
            self._tool_bar.Hide()

    def OnRun(self, e):
        raise NotImplementedError

    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, 'Algorithmic Trading System',
                               'Algorithmic Trading System', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()


def main():
    app = wx.App(False)
    MainFrame(None, title='Algorithmic Trading System').Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
