# *n*-layer perceptron for MNIST
#####Trains on 60,000 MNIST images, tests on 10,000 MNIST images

This is a from-scratch net that does not employ machine learning libraries.  Due to a state-oriented design (it was built to be extended into cognitive architectures), runtime is longer than most standard MNIST implementations (e.g. ~30 min train, <4 min test on 2 layers). 


## Run
Default *n* = 3, with to 784-node input, 60-node hidden, 10-node output (~93.7% accuracy). 

#### Use ./main.py to run

Layers can be adjusted in main.py:

    network_dimensions = [784, 60, 10]

Uncomment the following code block in nodenet/control.py to create a folder of learned digits, updated every 5k images:

    # # print images of digit recognition
    # if image_index % 5000 == 0:
    #   image_files = os.path.join(os.getcwd(), "image_files")
    #   if not os.path.exists(image_files):
    #       os.mkdir(image_files)
    #   _create_images(nodenet, image_files)

## Test
python -m unittest discover -v

(Requires mock 1.0.1)
