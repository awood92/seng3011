from datetime import datetime

class OrderBook:
	"""This is a data structure used for matching buys and sells"""
	buys = []
	sells = []

	def addToBuy(self,newRecord):
		self._insortBuy(newRecord)
		matchedOrders = self._matchOrders()
		return matchedOrders
	def addToSell(self,newRecord):

		self._insortSell(newRecord)
		matchedOrders = self._matchOrders()
		return matchedOrders
	def delete(self, recordToRemove): #returns True if deleted False otherwise

		valueToFind = None
		recordType = recordToRemove['Bid/Ask']
		if recordType == 'B':
			valueToFind = recordToRemove['Bid ID'] 
			for record in self.buys:
				if record['Bid ID'] == valueToFind:
					self.buys.remove(record)

					return True
		else:
			valueToFind = recordToRemove['Ask ID']
			for record in self.sells:
				if record['Ask ID'] == valueToFind:
					self.sells.remove(record)
					
					return True
		return False

	def amend(self,recordToAmend):
		#assert this later
		self.delete (recordToAmend)
		recordToAmend['Record Type'] = 'ENTER'
		recordType = recordToAmend['Bid/Ask']
		if recordType == 'B':
			self._insortBuy (recordToAmend)
		else:
			self._insortSell (recordToAmend)
		matchedOrders = self._matchOrders()
		return matchedOrders

	def _matchOrders(self): #This will go through buys and sells and return matched orders
		trades = []
		nextSell = 0
		finished = False
		buysToDelete = []
		for buyOrd in self.buys:
			sellsToDelete = []
			for nextSell in range(len(self.sells)):
				sellOrd = self.sells[nextSell]
				if (float(buyOrd['Price']) >= float(sellOrd['Price'])):
					# do the trades
					if int(buyOrd['Volume']) > int(sellOrd['Volume']):
						trades.append(self._createTrade(buyOrd,sellOrd,sellOrd['Volume']))
						buyOrd['Volume'] = str(int(buyOrd['Volume']) - int(sellOrd['Volume']))
						sellsToDelete.append(nextSell)
					elif int(buyOrd['Volume']) == int(sellOrd['Volume']):
						trades.append(self._createTrade(buyOrd,sellOrd,buyOrd['Volume']))
						sellsToDelete.append(nextSell)
						buysToDelete.append(buyOrd)
						break # this buy order is completed, move onto next one
					else:
						trades.append(self._createTrade(buyOrd,sellOrd,buyOrd['Volume']))
						sellOrd['Volume'] = str(int(sellOrd['Volume']) - int(buyOrd['Volume']))
						deleteBuy = True
						break # this buy order is completed, move onto next one
				else:
					finished = True
					break
			if len(sellsToDelete) > 0:
				for i in range(len(sellsToDelete)):
					self.sells.pop(sellsToDelete[i])
			if finished:
				break
		if len(buysToDelete) > 0:
			for i in range(len(buysToDelete)):
				self.buys.pop(buysToDelete[i])
		return trades

	def _createTrade(self,buyOrder,sellOrder,volume):
		trade = buyOrder.copy()
		trade['Record Type'] = "TRADE"
		trade['Price'] = sellOrder['Price']
		trade['Volume'] = volume	
		trade['Value'] = int(volume) * float(sellOrder['Price'])
		trade['Ask ID'] = sellOrder['Ask ID']
		trade['Bid/Ask'] = ""
		trade['Seller Broker ID'] = sellOrder['Seller Broker ID']
		return trade
		
	def _insortSell(self,record): #doesnt order by time
		count = 0
		insertPrice = record['Price']
		for order in self.sells:
			if insertPrice < order['Price']:
				break
			else:
				count+=1
		self.sells.insert(count,record)
	def _insortBuy(self,record): #doesnt order by time
		count = 0
		insertPrice = record['Price']
		for order in self.buys:
			if insertPrice > order['Price']:
				break
			else:
				count+=1
		self.buys.insert(count,record)
	def printBook(self):
		for item in self.buys:
			print item
		for item in self.sells:
			print item
