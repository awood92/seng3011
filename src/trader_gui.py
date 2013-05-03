#!/usr/bin/env python

"""Trader graphical user interface"""

import os
import csv
import wx

import yapsy.PluginManager

import trader
import plugins
import copy

import webbrowser

class MainFrame(wx.Frame):
    """The main window"""

    ID_EXPORT = 1
    ID_RUN = 2
    ID_EVALUATE = 3

    def __init__(self, *args, **kwargs):
        """Calls super, then InitUI"""
        super(MainFrame, self).__init__(*args, size=(800,600))
        self.InitUI()

    def InitUI(self):
        self.Centre()
        """Initialize the window"""
        HELP_STRINGS = {
            'Open': 'Open a market data file',
            'Export': 'Save outputted trades',
            'Close': 'Close the current market data file',
            'Exit': 'Terminate the program',
            'Statusbar': 'Toggle visibility of statusbar',
            'Toolbar': 'Toggle visibility of toolbar',
            'Run': 'Run trial',
            'About': 'Information about this program',
            'Show Evaluation': 'Preview evaluation after simulation is run'
        }
        self._statusbar = self.CreateStatusBar()
        self._toolbar = self.CreateToolBar()
        menu_bar = wx.MenuBar()
        menu = wx.Menu()
        item = menu.Append(wx.ID_OPEN, '&Open\tCtrl+O', HELP_STRINGS['Open'])
        self.Bind(wx.EVT_MENU, self.OnOpen, item)
        self._item_export = menu.Append(wx.ID_ANY, '&Export',
                                        HELP_STRINGS['Export'])
        self.Bind(wx.EVT_MENU, self.OnExport, self._item_export)
        menu.AppendSeparator()
        self._item_close = menu.Append(wx.ID_CLOSE, '&Close\tCtrl+W',
                                       HELP_STRINGS['Close'])
        self.Bind(wx.EVT_MENU, self.OnClose, self._item_close)
        item = menu.Append(wx.ID_EXIT, 'E&xit\tCtrl+Q', HELP_STRINGS['Exit'])
        self.Bind(wx.EVT_MENU, self.OnExit, item)
        menu_bar.Append(menu, '&File')
        menu = wx.Menu()
        self._item_statusbar = menu.Append(wx.ID_ANY, 'Show &Statusbar',
                                            HELP_STRINGS['Statusbar'],
                                            wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self._item_statusbar)
        menu.Check(self._item_statusbar.GetId(), True)
        self._item_toolbar = menu.Append(wx.ID_ANY, 'Show &Toolbar',
                                          HELP_STRINGS['Toolbar'],
                                          wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.ToggleToolBar, self._item_toolbar)
        menu.Check(self._item_toolbar.GetId(), True)
        menu_bar.Append(menu, '&View')
        menu = wx.Menu()
        self._item_run = menu.Append(wx.ID_ANY, '&Run', HELP_STRINGS['Run'])
        self.Bind(wx.EVT_MENU, self.OnRun, self._item_run)
        menu_bar.Append(menu, '&Tools')
        menu = wx.Menu()
        item = menu.Append(wx.ID_ABOUT, '&About', HELP_STRINGS['About'])
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        menu_bar.Append(menu, '&Help')
        self.SetMenuBar(menu_bar)
        icon = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN)
        tool = self._toolbar.AddLabelTool(wx.ID_OPEN, 'Open', icon,
                                           shortHelp='Open',
                                           longHelp=HELP_STRINGS['Open'])
        self.Bind(wx.EVT_TOOL, self.OnOpen, tool)
        icon = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS)
        tool = self._toolbar.AddLabelTool(MainFrame.ID_EXPORT, 'Export',
                                           icon, shortHelp='Export',
                                           longHelp=HELP_STRINGS['Export'])
        self.Bind(wx.EVT_TOOL, self.OnExport, tool)
        self._toolbar.AddSeparator()
        icon = wx.ArtProvider.GetBitmap(wx.ART_CROSS_MARK)
        tool = self._toolbar.AddLabelTool(wx.ID_CLOSE, 'Close', icon,
                                           shortHelp='Close',
                                           longHelp=HELP_STRINGS['Close'])
        self.Bind(wx.EVT_TOOL, self.OnClose, tool)
        self._toolbar.AddSeparator()
        icon = wx.Bitmap(my_path('resources/run.png'))
        tool = self._toolbar.AddLabelTool(MainFrame.ID_RUN, 'Run',
                                           icon, shortHelp='Run',
                                           longHelp=HELP_STRINGS['Run'])
        self.Bind(wx.EVT_TOOL, self.OnRun, tool)
        self._toolbar.AddSeparator()
        icon = wx.Bitmap(my_path('resources/evaluate.png'))
        tool = self._toolbar.AddLabelTool(MainFrame.ID_EVALUATE, 'Show Evaluation',
                                           icon, shortHelp='Show Evaluation',
                                           longHelp=HELP_STRINGS['Show Evaluation'])
        self.Bind(wx.EVT_TOOL, self.OnShowEvaluation, tool)
        self._toolbar.Realize()
        self._enable_controls(False)
        panel = wx.Panel(self)
        self._notebook = wx.Notebook(panel)
        sizer = wx.BoxSizer()
        sizer.Add(self._notebook, 1, wx.EXPAND)
        panel.SetSizer(sizer)

    def _enable_controls(self, enable=True):
        self._item_export.Enable(enable)
        self._item_close.Enable(enable)
        self._item_run.Enable(enable)
        self._toolbar.EnableTool(MainFrame.ID_EXPORT, enable)
        self._toolbar.EnableTool(wx.ID_CLOSE, enable)
        self._toolbar.EnableTool(MainFrame.ID_RUN, enable)

    def OnOpen(self, e):
        """Open market data file"""
        wildcard = 'CSV files (*.csv)|*.csv|Text files (*.txt)|*.txt|' \
                   'All files (*.*)|*.*'
        dialog = wx.FileDialog(self, wildcard=wildcard,
                               style=wx.OPEN|wx.MULTIPLE)
        count = self._notebook.GetPageCount()
        if dialog.ShowModal() == wx.ID_OK:
            for path in dialog.GetPaths():
                panel = TabPanel(self._notebook)
                panel.Open(path)
                self._notebook.AddPage(panel, os.path.basename(path), True)
        if count == 0 and self._notebook.GetPageCount() > 0:
            self._enable_controls()
        dialog.Destroy()

    def OnExport(self, e):
        """Save algorithmic trades"""
        wildcard = 'CSV files (*.csv)|*.csv|Text files (*.txt)|*.txt|' \
                   'All files (*.*)|*.*'
        dialog = wx.FileDialog(self, wildcard=wildcard, style=wx.SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            self._notebook.GetCurrentPage().Export(dialog.GetPath())
        dialog.Destroy()

    def OnClose(self, e):
        """Close the current market data file"""
        self._notebook.DeletePage(self._notebook.GetSelection())
        if self._notebook.GetPageCount() == 0:
            self._enable_controls(False)

    def OnExit(self, e):
        """Exit the program"""
        close = True
        if self._notebook.GetPageCount() > 0:
            dialog = wx.MessageDialog(self, 'Close all tabs?', 'Quit')
            if dialog.ShowModal() != wx.ID_OK:
                close = False
            dialog.Destroy()
        if close:
            self.Close(True)

    def ToggleStatusBar(self, e):
        """Toggle the statusbar visibility"""
        if self._item_statusbar.IsChecked():
            self._statusbar.Show()
        else:
            self._statusbar.Hide()

    def ToggleToolBar(self, e):
        """Toggle the toolbar visibility"""
        if self._item_toolbar.IsChecked():
            self._toolbar.Show()
        else:
            self._toolbar.Hide()

    def OnRun(self, e):
        """Run the simulation"""
        self._enable_controls(False)
        self._notebook.GetCurrentPage().Run()
        self._enable_controls(True)
        
    def OnShowEvaluation(self, e):
        """Show the evaluation"""
        new = 2
        url = "http://127.0.0.1:8000/evaluator/"
        webbrowser.open(url,new=new)
        
    def OnAbout(self, e):
        """About the program"""
        dialog = wx.MessageDialog(self, 'Algorithmic Trading System',
                                  'Algorithmic Trading System', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()


class TabPanel(wx.Panel):
    """A workspace for a given market data file"""

    def __init__(self, *args, **kwargs):
        """Calls super, then InitUI"""
        super(TabPanel, self).__init__(*args, **kwargs)
        self.InitUI()

    def InitUI(self):
        """Initialize the workspace"""
        plugin_manager = yapsy.PluginManager.PluginManager()
        plugin_manager.setPluginPlaces([my_path('plugins')])
        plugin_manager.setCategoriesFilter({
            'SignalGenerator': plugins.ISignalGeneratorPlugin,
            'Engine': plugins.IEnginePlugin,
            'StrategyEvaluator': plugins.IStrategyEvaluatorPlugin,
        })
        plugin_manager.collectPlugins()
        category_plugins = plugin_manager.getPluginsOfCategory('SignalGenerator')
        self._signal_generators = {}
        for plugin in category_plugins:
            plugin_settings = TabPanel._plugin_settings(plugin)
            self._signal_generators[plugin.details.get('Core', 'Name')] = plugin_settings
        category_plugins = plugin_manager.getPluginsOfCategory('Engine')
        self._engines = {}
        for plugin in category_plugins:
            plugin_settings = TabPanel._plugin_settings(plugin)
            self._engines[plugin.details.get('Core', 'Name')] = plugin_settings
        category_plugins = plugin_manager.getPluginsOfCategory('StrategyEvaluator')
        self._strategy_evaluators = {}
        for plugin in category_plugins:
            plugin_settings = TabPanel._plugin_settings(plugin)
            self._strategy_evaluators[plugin.details.get('Core', 'Name')] = plugin_settings
        grid = wx.FlexGridSizer(4, 4, 3, 3)
        self._signal_generator = self._add_plugin(grid, 'Signal Generator',
                                                  self._signal_generators.keys(),
                                                  self.OnConfigSignalGenerator,
                                                  self.OnAboutSignalGenerator)
        self._engine = self._add_plugin(grid, 'Engine',
                                        self._engines.keys(),
                                        self.OnConfigEngine,
                                        self.OnAboutEngine)
        self._strategy_evaluator = self._add_plugin(grid, 'Strategy Evaluator',
                                                    self._strategy_evaluators.keys(),
                                                    self.OnConfigStrategyEvaluator,
                                                    self.OnAboutStrategyEvaluator)
        box = wx.BoxSizer()
        box.Add(grid, 1, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(box)

    @staticmethod
    def _plugin_settings(plugin):
        if plugin.details.has_section('Parameters'):
            default = dict(plugin.details.items('Parameters'))
        else:
            default = {}
        return {'plugin': plugin, 'default': default}

    def _add_plugin(self, grid, name, choices, on_config, on_about):
        text = wx.StaticText(self, label=name+':')
        label = ''
        if len(choices) > 0:
            label = choices[0]
        combo_box = wx.ComboBox(self, wx.ID_ANY, label, choices=choices)
        config = wx.Button(self, label='Configure')
        about = wx.Button(self, label='About')
        self.Bind(wx.EVT_BUTTON, on_config, config)
        self.Bind(wx.EVT_BUTTON, on_about, about)
        row = [
            (text, 1, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL),
            (combo_box, 1, wx.EXPAND),
            config,
            about
        ]
        grid.AddMany(row)
        return combo_box

    def Open(self, path):
        """Open the market data file"""
        market_data = open(path)
        dict_reader = csv.DictReader(market_data)
        self._market_data = [line for line in dict_reader]
        self._fieldnames = dict_reader.fieldnames
        market_data.close()

    def Export(self, path):
        """Export the algorithmic trades file"""
        if self._trades is None:
            self.Run()
        export = open(path, 'w')
        dict_writer = csv.DictWriter(export, self._fieldnames)
        fieldnames = {}
        for fieldname in self._fieldnames:
            fieldnames[fieldname] = fieldname
        dict_writer.writerow(fieldnames)
        dict_writer.writerows(trades)
        export.close()

    def Run(self):
        """Run the simulation"""
        plugin_name = self._signal_generator.GetValue()
        plugin = self._signal_generators[plugin_name]['plugin']
        signal_generator = plugin.plugin_object
        signal_generator.setup(plugin.details)
        plugin_name = self._engine.GetValue()
        plugin = self._engines[plugin_name]['plugin']
        engine = plugin.plugin_object
        engine.setup(plugin.details)
        plugin_name = self._strategy_evaluator.GetValue()
        plugin = self._strategy_evaluators[plugin_name]['plugin']
        strategy_evaluator = plugin.plugin_object
        strategy_evaluator.setup(plugin.details)
        
        progressMax = len(self._market_data)
        progressdialog = wx.ProgressDialog("Running Simulation", "Trading records remaining", progressMax ,  style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
        progressdialog.Update(0,"Preparing data for processing.\nSimulation will begin shortly.")
        self._trades = trader.run_trial(copy.deepcopy(self._market_data), signal_generator,
                                        engine, strategy_evaluator, progressdialog)
        progressdialog.Destroy()
    
    def _config(self, control, plugins):
        plugin_name = control.GetValue()
        if plugin_name in plugins:
            plugin = plugins[plugin_name]
            if plugin['plugin'].details.has_section('Parameters'):
                config = dict(plugin['plugin'].details.items('Parameters'))
            else:
                config = {}
            dialog = ConfigDialog(None, title=plugin_name+' Configuration')
            dialog.InitUI(config, plugin['default'])
            if dialog.ShowModal() == wx.ID_OK:
                for name, value in dialog.config.iteritems():
                    plugin['plugin'].details.set('Parameters', name, value)
            dialog.Destroy()
        else:
            dialog = wx.MessageDialog(self,
                                      'Please choose a plugin to configure',
                                      'No plugin chosen', wx.OK)
            dialog.ShowModal()
            dialog.Destroy()

    def _about(self, control, plugins):
        message = 'Please choose a plugin'
        caption = 'No plugin chosen'
        plugin_name = control.GetValue()
        if plugin_name in plugins:
            plugin = plugins[plugin_name]['plugin']
            caption = plugin.name
            message = plugin.description
        dialog = wx.MessageDialog(self, message, caption, wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

    def OnConfigSignalGenerator(self, e):
        """Show modal configure dialog"""
        self._config(self._signal_generator, self._signal_generators)

    def OnAboutSignalGenerator(self, e):
        """Show modal about dialog"""
        self._about(self._signal_generator, self._signal_generators)

    def OnConfigEngine(self, e):
        """Show modal configure dialog"""
        self._config(self._engine, self._engines)

    def OnAboutEngine(self, e):
        """Show modal about dialog"""
        self._about(self._engine, self._engines)

    def OnConfigStrategyEvaluator(self, e):
        """Show modal configure dialog"""
        self._config(self._strategy_evaluator, self._strategy_evaluators)

    def OnAboutStrategyEvaluator(self, e):
        """Show modal about dialog"""
        self._about(self._strategy_evaluator, self._strategy_evaluators)


class ConfigDialog(wx.Dialog):
    """Plugin configuration dialog"""

    def InitUI(self, config, default):
        """Initialize the dialog"""
        grid = wx.FlexGridSizer(2, 1, 5, 5)
        fields = wx.FlexGridSizer(0, 2)
        self._fields = {}
        self._config = config
        self._default = default
        for name, value in config.iteritems():
            text = wx.StaticText(self, label=name)
            self._fields[name] = wx.TextCtrl(self, value=value)
            row = [
                (text, 1, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL),
                (self._fields[name], 1, wx.EXPAND)
            ]
            fields.AddMany(row)
        ok = wx.Button(self, wx.ID_OK)
        cancel = wx.Button(self, wx.ID_CANCEL)
        default = wx.Button(self, label='Default')
        self.Bind(wx.EVT_BUTTON, self.OnOk, ok)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, cancel)
        self.Bind(wx.EVT_BUTTON, self.OnDefault, default)
        buttons = wx.GridSizer(1, 3, 3, 3)
        row = [
            (ok, 1, wx.EXPAND),
            (cancel, 1, wx.EXPAND),
            (default, 1, wx.EXPAND)
        ]
        buttons.AddMany(row)
        grid.AddMany([fields, buttons])
        self.SetSizer(grid)

    def OnOk(self, e):
        """Close the window and return ok"""
        for name in self._fields:
            self._config[name] = self._fields[name].GetValue()
        self.EndModal(wx.ID_OK)

    def OnCancel(self, e):
        """Close the window and return cancel"""
        self.EndModal(wx.ID_CANCEassignmentL)

    def OnDefault(self, e):
        """Reset entered values to default"""
        for name, value in self._default.iteritems():
            self._fields[name].SetValue(value)

    @property
    def config(self):
        """User specified configuration"""
        return self._config


def my_path(path):
    """Path to use, given the relative path"""
    return os.path.join(os.path.dirname(__file__), path)


def main():
    """Open the main window"""
    app = wx.App(False)
    MainFrame(None, title='Algorithmic Trading System').Show()
    app.MainLoop()
    
if __name__ == '__main__':
    main()
