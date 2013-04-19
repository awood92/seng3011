"""Initial signal generator plugin"""

import plugins


class InitialSignalGenerator(plugins.ISignalGeneratorPlugin):
    """Makes a buy order and a sell order at predefined times"""

    def setup(self, config):
        """Read buy and sell parameters from the config file"""
        self.started = False
        buy = {
            'Instrument': config.get('Parameters', 'instrument'),
            'Date': config.getint('Parameters', 'buy_date'),
            'Time': config.get('Parameters', 'buy_time'),
            'Record Type': 'ENTER',
            'Price': config.get('Parameters', 'price'),
            'Volume': config.getint('Parameters', 'volume'),
            'Undisclosed Volume': config.getint('Parameters', 'undisclosed_volume'),
            'Value': '',
            'Qualifiers': '',
            'Trans ID': 0,
            'Bid ID': 'Algorithmic1',
            'Ask ID': '',
            'Bid/Ask': 'B',
            'Entry Time': '',
            'Old Price': '',
            'Old Volume': '',
            'Buyer Broker ID': 'Algorithmic',
            'Seller Broker ID': ''
        }
        sell = buy.copy()
        sell['Date'] = config.get('Parameters', 'sell_date')
        sell['Time'] = config.get('Parameters', 'sell_time')
        sell['Bid/Ask'] = 'A'
        sell['Buyer Broker ID'] = ''
        sell['Seller Broker ID'] = 'Algorithmic'
        sell['Bid ID'] = ''
        sell['Ask ID'] = 'Algorithmic1'
        if (sell['Date'], sell['Time']) < (buy['Date'], buy['Time']):
            self.orders = [sell, buy]
        else:
            self.orders = [buy, sell]

    def __call__(self, trading_record=None):
        orders = []
        if not self.started:
            self.started = True
            orders = self.orders
        return orders
