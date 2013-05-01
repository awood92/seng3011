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
        ID_EXPORT = 1
        ID_RUN = 2
        HELP_STRINGS = {
            'Open': 'Open a market data file',
            'Export': 'Save outputted trades',
            'Close': 'Close the current market data file',
            'Exit': 'Terminate the program',
            'Statusbar': 'Toggle visibility of statusbar',
            'Toolbar': 'Toggle visibility of toolbar',
            'Run': 'Run trial',
            'About': 'Information about this program'
        }
        self._status_bar = self.CreateStatusBar()
        self._tool_bar = self.CreateToolBar()
        menu_bar = wx.MenuBar()
        menu = wx.Menu()
        item = menu.Append(wx.ID_OPEN, '&Open\tCtrl+O', HELP_STRINGS['Open'])
        self.Bind(wx.EVT_MENU, self.OnOpen, item)
        self._item_export = menu.Append(wx.ID_ANY, '&Export',
                                        HELP_STRINGS['Export'])
        self.Bind(wx.EVT_MENU, self.OnExport, self._item_export)
        self._item_export.Enable(False)
        menu.AppendSeparator()
        self._item_close = menu.Append(wx.ID_CLOSE, '&Close\tCtrl+W',
                                       HELP_STRINGS['Close'])
        self.Bind(wx.EVT_MENU, self.OnClose, self._item_close)
        self._item_close.Enable(False)
        item = menu.Append(wx.ID_EXIT, 'E&xit\tCtrl+Q', HELP_STRINGS['Exit'])
        self.Bind(wx.EVT_MENU, self.OnExit, item)
        menu_bar.Append(menu, '&File')
        menu = wx.Menu()
        self._item_status_bar = menu.Append(wx.ID_ANY, 'Show &Statusbar',
                                            HELP_STRINGS['Statusbar'],
                                            wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self._item_status_bar)
        menu.Check(self._item_status_bar.GetId(), True)
        self._item_tool_bar = menu.Append(wx.ID_ANY, 'Show &Toolbar',
                                          HELP_STRINGS['Toolbar'],
                                          wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.ToggleToolBar, self._item_tool_bar)
        menu.Check(self._item_tool_bar.GetId(), True)
        menu_bar.Append(menu, '&View')
        menu = wx.Menu()
        self._item_run = menu.Append(wx.ID_ANY, '&Run', HELP_STRINGS['Run'])
        self.Bind(wx.EVT_MENU, self.OnRun, self._item_run)
        self._item_run.Enable(False)
        menu_bar.Append(menu, '&Tools')
        menu = wx.Menu()
        item = menu.Append(wx.ID_ABOUT, '&About', HELP_STRINGS['About'])
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        menu_bar.Append(menu, '&Help')
        self.SetMenuBar(menu_bar)
        icon = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN)
        tool = self._tool_bar.AddLabelTool(wx.ID_OPEN, 'Open', icon,
                                           shortHelp='Open',
                                           longHelp=HELP_STRINGS['Open'])
        self.Bind(wx.EVT_TOOL, self.OnOpen, tool)
        icon = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS)
        tool = self._tool_bar.AddLabelTool(ID_EXPORT, 'Export', icon,
                                           shortHelp='Export',
                                           longHelp=HELP_STRINGS['Export'])
        self.Bind(wx.EVT_TOOL, self.OnExport, tool)
        self._tool_bar.AddSeparator()
        icon = wx.ArtProvider.GetBitmap(wx.ART_CROSS_MARK)
        tool = self._tool_bar.AddLabelTool(wx.ID_CLOSE, 'Close', icon,
                                           shortHelp='Close',
                                           longHelp=HELP_STRINGS['Close'])
        self.Bind(wx.EVT_TOOL, self.OnClose, tool)
        self._tool_bar.AddSeparator()
        icon = wx.Bitmap('resources/run.png')
        tool = self._tool_bar.AddLabelTool(ID_RUN, 'Run', icon,
                                           shortHelp='Run',
                                           longHelp=HELP_STRINGS['Run'])
        self.Bind(wx.EVT_TOOL, self.OnRun, tool)
        self._tool_bar.EnableTool(wx.ID_CLOSE, False)
        self._tool_bar.EnableTool(ID_EXPORT, False)
        self._tool_bar.EnableTool(ID_RUN, False)

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


class TabPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(TabPanel, self).__init__(self, *args, **kwargs)
        self.InitUI()

    def InitUI(self):
        pass


def main():
    app = wx.App(False)
    MainFrame(None, title='Algorithmic Trading System').Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
