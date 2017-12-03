# *n*-layer perceptron for MNIST
**Trains on 60,000 MNIST images, tests on 10,000 MNIST images**

This is a from-scratch net that does not employ machine learning libraries.  Due to a state-oriented design (it was built to be extended into cognitive architectures), runtime is longer than most standard MNIST implementations (e.g. ~30 min train, <4 min test on 2 layers). 


## Run
Use the following command to specify network dimensions, build, run, and test an *n*-layer MNIST classifier:

#### ./main.py 784,...,10

For example, the following input will build a 3-layer classifier with 784 input nodes, 60 hidden nodes, and 10 output nodes:

    ./main.py 784,60,10

Uncomment the following code block in nodenet/control.py to create a folder of final learned digit representations (works for 2 layers only):

	# # print images of final learned digits
	# if run_type == "test" and image_index == 0:
	# 	_create_images(nodenet)

You can also save your own net ([dill](https://pypi.python.org/pypi/dill) required) by uncommenting this line in main.py under "TEST" before running:

    # config.save_weights(nodenet, network_dimensions)

To test a saved net, follow the directions in the "Demo" section, replacing *demo* in the command with its input dimensions.

## Demo
Pretrained nets are available for demo on the testing data.  (This requires [dill](https://pypi.python.org/pypi/dill), which can be quickly acquired with *pip install dill*.)

The pretrained nets can be called with the following command, where *demo* is the specifications of the desired pretrained net:

#### ./main.py *demo* pretrain

For example, the following input will run a pretrained 2-layer classifier on the MNIST testing data:

    ./main.py 784,10 pretrain

Available pretrained nets:

* 784,60,10 *(~93.7% accuracy)*
* 784,10 *(~91.7% accuracy)*

## Unit Test

#### python -m unittest discover -v

(Requires mock 1.0.1)
