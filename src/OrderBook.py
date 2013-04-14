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
		finished = false
		for buyOrd in self.buys:
			for nextSell in range(len(self.sells)):
				sellOrd = self.sells[nextSell]
				if buyOrd['Price'] >= self.sells
					# do trades
					if buyOrd['Volume'] >= sellOrd['Volume']:
						#buyOrd['Volume'] -= sellOrd['Volume']
						#create a trade
						#remove the sell order somehow
					else:
						#create a trade
						#reduce the volume of the sell order: sellOrd['Volume'] -= buyOrd['Volume']
						#remove the buy order
				else:
					finished = true
			if finished:
				break
				
		return trades
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
