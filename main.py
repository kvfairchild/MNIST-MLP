#!/usr/bin/env python
from datetime import timedelta
import numpy as np
import time
import sys

from nodenet import config
from nodenet import control
from nodenet.nodenet import Nodenet
from nodenet.file_parser import MNIST_file_parser

def build_nodenet(nodenet, network_dimensions):

	node_data = config.generate_node_data(network_dimensions)
	config.add_nodes(nodenet, node_data)

	link_data = config.generate_link_data(nodenet)
	config.link_nodes(nodenet, link_data)

	return network_dimensions

def parse_data(data_type):
	return MNIST_file_parser.read(data_type)

def run_nodenet(nodenet, data, run_type):
	start_time = time.time()

	images = data["images"]
	labels = data["labels"]

	# feed images into network
	for i, image in enumerate(images):

		if i < 1000: 
			config.set_activation(nodenet, image)
			control.run(nodenet, labels[i], i, run_type)

	print "execution time: ", str(timedelta(seconds=(time.time()-start_time)))


if __name__ == "__main__":

	if len(sys.argv) == 1:
		raise ValueError("please enter network dimensions as " + 
			"comma separated values without spaces (i.e. 784,60,10)")
	else:

		network_dimensions = [int(i) for i in sys.argv[1].split(",")]

		nodenet = Nodenet()
		build_nodenet(nodenet, network_dimensions)

	if len(sys.argv) == 2:

		# TRAIN
		data = parse_data("training")
		run_nodenet(nodenet, data, "train")
		# config.save_weights(nodenet, network_dimensions) # save trained network

		# TEST
		data = parse_data("testing")
		run_nodenet(nodenet, data, "test")

	elif len(sys.argv) == 3 and sys.argv[2] == "pretrain":

		# PRETRAINED NET (TEST)
		data = parse_data("testing")
		config.initialize_net(nodenet, network_dimensions)
		run_nodenet(nodenet, data, "test")
	
	else:
		raise ValueError("please enter a valid command")
