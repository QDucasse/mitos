class Token:

	def __init__(self, kind, value, position):
		self.kind = kind
		self.value = value
		self.position = position

	def __repr__(self):
		return self.kind
