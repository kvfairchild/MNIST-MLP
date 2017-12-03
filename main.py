#!/usr/bin/env python
from datetime import timedelta
import numpy as np
import time

from nodenet import config
from nodenet import control
from nodenet.nodenet import Nodenet
from nodenet.file_parser import MNIST_file_parser


def build_nodenet(nodenet):

	# enter nodes per layer
	network_dimensions = [784, 60, 10]

	node_data = config.generate_node_data(network_dimensions)
	config.add_nodes(nodenet, node_data)

	link_data = config.generate_link_data(nodenet)
	config.link_nodes(nodenet, link_data)

def parse_data(data_type):
	return MNIST_file_parser.read(data_type)

def run_nodenet(nodenet, data, run_type):
	start_time = time.time()

	images = data["images"]
	labels = data["labels"]

	# feed images into network
	for i, image in enumerate(images):

		config.set_activation(nodenet, image)
		control.run(nodenet, labels[i], i, run_type)

	print "execution time: ", str(timedelta(seconds=(time.time()-start_time)))


if __name__ == "__main__":
	nodenet = Nodenet()
	build_nodenet(nodenet)

	# TRAIN
	data = parse_data("training")
	run_nodenet(nodenet, data, "train")

	# TEST
	data = parse_data("testing")
	run_nodenet(nodenet, data, "test")
