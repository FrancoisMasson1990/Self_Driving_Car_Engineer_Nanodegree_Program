#The simulator captures images from three cameras mounted on the car: a center, right and left camera. That’s because of the issue of recovering from being off-center.

#Explanation of How Multiple Cameras Work
#The image below gives a sense for how multiple cameras are used to train a self-driving car. This image shows a bird's-eye perspective of the car. The driver is moving forward but wants to turn towards a destination on the left.

#From the perspective of the left camera, the steering angle would be less than the steering angle from the center camera. From the right camera's perspective, the steering angle would be larger than the angle from the center camera. The next section will discuss how this can be implemented in your project although there is no requirement to use the left and right camera images.

#During training, you want to feed the left and right camera images to your model as if they were coming from the center camera. This way, you can teach your model how to steer if the car drifts off to the left or the right.

#Figuring out how much to add or subtract from the center angle will involve some experimentation.

import csv
import cv2
import numpy as np 
from PIL import Image

lines = []

# Data file in opt because more space available 
# following line read data save in a csv file
with open('/opt/driving_log.csv') as csvfile :
    reader = csv.reader(csvfile)
    for line in reader:
        lines.append(line)

images=[]
measurements=[]

correction = 0.2 # this is a parameter to tune
for line in lines:
    img_center = np.asarray(Image.open(line[0]))
    img_left = np.asarray(Image.open(line[1]))
    img_right = np.asarray(Image.open(line[2]))
    images.append(img_center)
    images.append(img_left)
    images.append(img_right)
    steering_center = float(line[3])
    steering_left = steering_center + correction
    steering_right = steering_center - correction
    measurements.append(steering_center)
    measurements.append(steering_left)
    measurements.append(steering_right)

augmented_images, augmented_measurements=[],[]
for image,measurement in zip(images,measurements):
    augmented_images.append(image)
    augmented_measurements.append(measurement)
    augmented_images.append(cv2.flip(image,1))
    augmented_measurements.append(measurement*-1)