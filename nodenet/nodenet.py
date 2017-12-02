from uuid import uuid4

class Nodenet:
	def __init__(self, name = None):
		self.uid = uuid4()
		self.name = name
		self.learning_rate = .05
		self.RATE_DECAY = .0001
		self.node_dict = {}
		self.layers = []
		self.links_list = []

	@property
	def name(self):
	    return self.name if self.name else self.uid

	@name.setter
	def name(self, value):
	    self.name = value

	@property
	def node_dict(self, name):
		return self.node_dict[name]

	def add_layers(self, layers):
		self.layers = layers
		[self.add_nodes(layer) for layer in layers]

	def add_nodes(self, layer):
		[self.add_node(node) for node in layer]

	def add_node(self, node):
		self.node_dict[node.name] = node

