from __future__ import division
from itertools import groupby
from math import sqrt
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os

from .nodenet import Nodenet

def run(nodenet, target_output, image_index, run_type):
	output = _step_function(nodenet) # softmax output

	_pretty_print(output, target_output, image_index)

	if run_type == "train":
		_update_weights(nodenet, output, target_output, image_index)
	
	# # print images of final learned digits
	# if run_type == "test" and image_index == 0:
	# 	_create_images(nodenet)

	_zero_nodes(nodenet)
	_zero_gates(nodenet)
 
def _step_function(nodenet):

	for i, layer in enumerate(nodenet.layers):
		_net_function(nodenet)
		_link_function(nodenet)

		# fetch output from last layer
		if i == len(nodenet.layers)-1:
			output = [gate.activation for node in layer for gate in node.gate_vector]

	return _softmax(output) # apply softmax

# call node function for nodes that received activation
def _net_function(nodenet):
	node_dict = nodenet.node_dict

	for node in node_dict.values():
		for slot in node.slot_vector:
			if slot.activation != 0:
				node.node_function(slot.activation)
				slot.activation = 0

# multiply active node gate values with link weights, sum in target slots
def _link_function(nodenet):
	for layer in nodenet.links_list:
		for node in layer:
			for link in node:
				if link.origin_gate.is_active():
					_send_activation_to_target_slot(link)

# UPDATE LINK WEIGHTS

def _update_weights(nodenet, output, target_output, image_index):
	output_links = nodenet.links_list[len(nodenet.links_list)-1]
	learning_rate = _decay_learning_rate(nodenet)
	error_array = target_output - output

	# calculate and set weights for each link to output nodes
	for node_index, output_node in enumerate(output_links):
		error = error_array[node_index]

		for i in range(len(output_node)):
			link = output_node[i]

			# store weighted errors on link origin nodes
			link.origin_node.activation += link.weight * error * _tanh_deriv(link.origin_gate.activation)
			
			link.weight += learning_rate * link.origin_gate.activation * error

	if len(nodenet.links_list) > 1:
		_backprop(nodenet, learning_rate)

def _backprop(nodenet, learning_rate):
	i = len(nodenet.layers)-2

	while i > 0:
		prior_layer_links = _get_prior_layer_links(nodenet, i)

		for node_index, node in enumerate(nodenet.layers[i]):
			links = prior_layer_links[node_index]

			for link in links:
				error = link.target_node.activation

				# store weighted errors on link origin nodes
				link.origin_node.activation += link.weight * error * _tanh_deriv(link.origin_gate.activation)
				
				link.weight += learning_rate * link.origin_gate.activation * error
		i -= 1

def _decay_learning_rate(nodenet):
	learning_rate = nodenet.learning_rate
	RATE_DECAY = nodenet.RATE_DECAY

	nodenet.learning_rate = learning_rate * (learning_rate / (learning_rate + (learning_rate * RATE_DECAY)))
	
	return nodenet.learning_rate

# VISUALIZE LEARNED IMAGES

def _create_images(nodenet):
	image_files = os.path.join(os.getcwd(), "image_files")
	if not os.path.exists(image_files):
		os.mkdir(image_files)

	for node_index, node in enumerate(nodenet.layers[len(nodenet.layers)-1]):
		weight_matrix = [link.weight for link in nodenet.links_list[0][node_index]]
		chunk_length = int(sqrt(len(weight_matrix)))
		image = [weight_matrix[i:i+chunk_length] 
		for i in range(0, len(weight_matrix), chunk_length)]
		filepath = os.path.join(image_files, "node" + str(node_index) + ".png")

		plt.imshow(image, cmap="gray")
		plt.savefig(filepath)

# HELPER FUNCTIONS

def _pretty_print(output, target_output, image_index):
	predicted_int = _one_hot_to_int(output) # integer output
	target_int = _one_hot_to_int(target_output) # integer label

	global error_count
	error_count = 0 if image_index == 0 else error_count

	if predicted_int == target_int:
		print "#", image_index+1, "prediction: ", predicted_int, " target: ", target_int, "HIT"
	else:
		print "#", image_index+1, "prediction: ", predicted_int, " target: ", target_int
		error_count += 1
	
	success_rate = "{:.2f}".format((((image_index+1) - error_count) / (image_index+1)) * 100)
	print "success rate: ", success_rate, "%"

def _send_activation_to_target_slot(link):
	activation = link.origin_gate.activation * link.weight
	link.target_slot.activation = link.target_slot.activation + activation

def _softmax(output):
	exp_output = np.exp(output - np.max(output))
	return exp_output / exp_output.sum()

def _one_hot_to_int(one_hot):
	max_output = 0
	max_index = 0

	for node_index, node_output in enumerate(np.nditer(one_hot)):
		if node_output > max_output:
			max_output = node_output
			max_index = node_index

	return max_index

def _zero_gates(nodenet):
	for layer in nodenet.links_list:
		for node in layer:
			for link in node:
				link.origin_gate.activation = 0

# BACKPROP HELPERS

def _get_prior_layer_links(nodenet, i): # returns links connecting layeri nodes to layeri-1
	hidden_links = [link for node in nodenet.links_list[i-1] for link in node]

	# sort hidden layer links by target node
	key = lambda x: x.target_node
	hidden_links_by_target = sorted(hidden_links, key=key)
	
	return [list(g) for k, g in groupby(hidden_links_by_target, key)]

def _tanh_deriv(t):
	return 1.0 - np.tanh(t)**2

def _zero_nodes(nodenet): # resets node activation (which holds backprop value)
	for layer in nodenet.layers:
		for node in layer:
			node.activation = 0

