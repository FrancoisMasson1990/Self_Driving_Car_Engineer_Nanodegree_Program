# This code is an explanation of the video chapter 8 Training your Network and the reason of the code 

## When running the simulator, Data can be stored in tmpr file (csv + Image)
## In the csv file a directory is saved
# A match is needed if we want to extract the image 

# Using Python CSv library to read store the line from the drivinglog.csv file
# The best approach is to save the data on a local machine then export them on the worksapce GPU instance 

import csv
import cv2
# import numpy because that's the format require by Keras to process the image
import numpy as np 

lines = []
# Data file in opt because more space available 
# following line read data save in a csv file
with open('/driving_log.csv') as csvfile : # Directory of the csv file
    reader = csv.reader(csvfile)
    for line in reader:
        # For each line extract the path to the camera image
        lines.append(line)
        
images=[]
measurement=[]
for line in lines:
    source_path=line[0] # Get the directory file 
    filename = source_path.split('/')[-1] # Split and only keep the name of the image
    current_path ='../data/IMG/' + filename # Load the image desired
    image= cv2.imread(current_path) # Read the image
    images.append(image) # Load as an numpy array 
    measurement = float(line[3]) # Load the value of the steering angle
    measurements.append(measurement) # add to a list
    
# Implementing a NN first attempt 
# The output label is in this case the value of the steering angle

X_train = np.array(images)
y_train = np.array(measurements)

from keras.models import Sequential
from keras.layers import Flatten,Dense
# Simple NN possible 
# Just a flatten image connected to one output value
# In this case we are not in a CNN classification we are in a regression model
# reduce the error of the steering angle
# We don't use softmax function
model = Sequential()
model.add(Flatten(input_shape=(160,320,3))) # Size of the recorded image in RGB
model.add(Dense(1))

model.compile(loss='mse',optimizer='adam') # mean square error 
model.fit(X_train,y_train,validation_split=0.2,shuffle=True)# shuffle the data and split in train and validation set

#load in a model h5
model.save('model.h5')

# Validating Your Network
#In order to validate your network, you'll want to compare model performance on the training set and a validation set. The validation set should contain image and steering data that was not used for training. A rule of thumb could be to use 80% of your data for training and 20% for validation or 70% and 30%. Be sure to randomly shuffle the data before splitting into training and validation sets.

#If model predictions are poor on both the training and validation set (for example, mean squared error is high on both), then this is evidence of underfitting. Possible solutions could be to increase the number of epochs add more convolutions to the network.

#When the model predicts well on the training set but poorly on the validation set (for example, low mean squared error for training set, high mean squared error for validation set), this is evidence of overfitting. If the model is overfitting, a few ideas could be to use dropout or pooling layers use fewer convolution or fewer fully connected layers collect more data or further augment the data set

#Ideally, the model will make good predictions on both the training and validation sets. The implication is that when the network sees an image, it can successfully predict what angle was being driven at that moment. 
