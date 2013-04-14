class OrderBook:
	"""This is a data structure used for matching buys and sells"""
	buys = []
	sells = []
	def __init__(self, arg):
		super(OrderBook, self).__init__()
		self.arg = arg
	def addToBuy(self,newRecord):
		_insort(newRecord,self.buys)
		trades = _matchOrders()
		return trades
	def addToSell(self,newRecord):
		_insort(newRecord,self.sells)
		trades = _matchOrders()
		return trades
	def removeBuys(self, recordToRemove):
		pass
	def removeBuys(self, recordToRemove):
		pass
	def _matchOrders(): #This will go through buys and sells and return matched orders
		trades = []
		return trades
	def _insort(record,arr):
		count = 0
		insertPrice = record['Price']
		for order in arr:
			if insertPrice < order['Price']:
				arr.insert(record,count)
				break
			else:
				count+=1