class handgun:
	def __init__(self,manufacturer, model, guntype, caliber, size, action, capacity, minprice,maxprice,comments,photo):
		self.manufacturer = manufacturer
		self.model = model
		self.guntype = guntype
		self.caliber = caliber
		self.size = size
		self.action = action
		self.capacity = capacity
		self.minprice = minprice
		self.maxprice = maxprice
		self.comments = comments
		self.photo = photo

	def average_price(self):
		return (self.minprice + self.maxprice) / 2

	def tostring(self):
		print self.model, self.manufacturer