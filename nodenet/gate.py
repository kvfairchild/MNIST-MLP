from math import tanh
import numpy as np

class Gate:
    def __init__(self, name, activation, parameters=None, gate_function=None):
        self.name = name
        self.activation = activation
        self.parameters = parameters if parameters else {}
        self.gate_function = {
			"default": self._default_gate_function,
			"output": self._output_gate_function
		}[gate_function]

    def _default_gate_function(self, activation):
    	self.activation = tanh(activation)

    def _output_gate_function(self, activation):
    	self.activation = activation

    def is_active(self):
        return self.activation > self.parameters.get("threshold")
