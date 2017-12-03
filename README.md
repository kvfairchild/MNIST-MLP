# *n*-layer perceptron for MNIST
**Trains on 60,000 MNIST images, tests on 10,000 MNIST images**

This is a from-scratch net that does not employ machine learning libraries.  Due to a state-oriented design (it was built to be extended into cognitive architectures), runtime is longer than most standard MNIST implementations (e.g. ~30 min train, <4 min test on 2 layers). 


## Run
Default *n* = 3, with to 784-node input, 60-node hidden, 10-node output (~93.7% accuracy). 

#### Use ./main.py to run

Layers can be adjusted in main.py:

    network_dimensions = [784, 60, 10]

Set optimal initialization in link.py (default 3+ layers):

    # OPTIMAL WEIGHT INITIALIZATION 
    
    # 2 layers:
    # self.weight = weight if weight is not None else weight == 0

    # 3+ layers:
    self.weight = weight if weight is not None else random.uniform(-.25, .25)

Uncomment the following code block in nodenet/control.py to create a folder of final learned digit representations (works for 2 layers only):

	# # print images of final learned digits
	# if run_type == "test" and image_index == 0:
	# 	_create_images(nodenet)

## Test
python -m unittest discover -v

(Requires mock 1.0.1)
