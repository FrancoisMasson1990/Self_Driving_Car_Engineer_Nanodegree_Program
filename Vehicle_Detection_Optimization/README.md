# Vehicle Detection Optimization

### Weight files

You can download the weight from [here](https://drive.google.com/open?id=0B5WIzrIVeL0WS3N2VklTVmstelE) and save it to
the [weights](weights) folder.

### Neural Network Approach (YOLO)

YOLO is an object detection pipeline baesd on Neural Network. Contrast to prior work on object detection with classifiers to perform detection, YOLO frame object detection as a regression problem to spatially separated bounding boxes and associated class probabilities. A single neural network predicts bounding boxes and class probabilities directly from full images in one evaluation. Since the whole detection pipeline is a single network, it can be optimized end-to-end directly on detection performance. 

The present work was inspired by previous work from :
https://junshengfu.github.io
