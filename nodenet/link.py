import uuid
import random


class Link:
    def __init__(self, origin_node, origin_gate, target_node, target_slot, weight=None):  
        self.uid = uuid.uuid4()
        self.origin_node = origin_node
        self.origin_gate = origin_gate
        self.target_node = target_node
        self.target_slot = target_slot
        self.weight = weight if weight is not None else random.uniform(-.25, .25)
