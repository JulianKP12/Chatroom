class Connection:
	def __init__(self, name, client, addr):
		self.name = name
		self.client = client
		self.addr = addr

	def __repr__(self):
		return f"Connection({name}, {addr[0]}:{addr[1]})"