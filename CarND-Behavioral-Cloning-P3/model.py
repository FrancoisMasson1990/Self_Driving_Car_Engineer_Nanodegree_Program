### Importation of the different module
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

correction = 0.5 # this is a parameter to tune

# Data augmentation 

for line in lines:
    #source_path=line[0]
    #filename = source_path.split('/')[-1]
    #current_path ='/opt/IMG/' + filename 
    
    ## Using left right and center Camera and add the steering value depending on the side of the camera
    ## One of the reason is to keep data augmentation
    img_center = np.asarray(Image.open(line[0]))
    img_left = np.asarray(Image.open(line[1]))
    img_right = np.asarray(Image.open(line[2]))
    #image= cv2.imread(current_path)
    images.append(img_center)
    images.append(img_left)
    images.append(img_right)
    #measurement = float(line[3])
    steering_center = float(line[3])
    steering_left = steering_center + correction
    steering_right = steering_center - correction
    measurements.append(steering_center)
    measurements.append(steering_left)
    measurements.append(steering_right)
    
#Flipping Images And Steering Measurements
augmented_images, augmented_measurements=[],[]
for image,measurement in zip(images,measurements):
    augmented_images.append(image)
    augmented_measurements.append(measurement)
    augmented_images.append(cv2.flip(image,1))
    augmented_measurements.append(measurement*-1)
    
X_train = np.array(images)
y_train = np.array(measurements)

from keras.models import Sequential
from keras.layers import Flatten,Dense, Lambda
from keras.layers.convolutional import Convolution2D
from keras.layers import Conv2D
from keras.layers.pooling import MaxPooling2D
from keras.layers import Cropping2D
from keras.layers import Dropout
from keras.layers import MaxPooling2D

### Cropping 
#The cameras in the simulator capture 160 pixel by 320 pixel images.
#Not all of these pixels contain useful information, however. In the image above, the top portion of the image captures trees and hills and sky, and the bottom portion of the image captures the hood of the car.
#Your model might train faster if you crop each image to focus on only the portion of the image that is useful for predicting a steering angle


model = Sequential()
model.add(Lambda(lambda x: x /255.0 -0.5, input_shape=(160,320,3)))
#The example below crops:
#75 rows pixels from the top of the image
#25 rows pixels from the bottom of the image
#0 columns of pixels from the left of the image
#0 columns of pixels from the right of the image
model.add(Cropping2D(cropping=((75,25), (0,0))))
model.add(Conv2D(filters=24, kernel_size=5, strides=(2,2), padding='same', activation='relu'))
model.add(Conv2D(filters=36, kernel_size=5, strides=(2,2), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=4))
model.add(Conv2D(filters=48, kernel_size=5, strides=(2,2), padding='same', activation='relu'))
model.add(Conv2D(filters=64, kernel_size=3, padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=64, kernel_size=3, padding='same', activation='relu'))
#this is evidence of overfitting. 
#If the model is overfitting, a few ideas could be to use dropout or pooling layers
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(1164, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(100, activation='relu'))
model.add(Dense(50, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(1, activation='tanh'))

model.compile(loss='mse',optimizer='adam')
#randomly shuffle the data before splitting into training and validation sets.
history_object = model.fit(X_train,y_train,validation_split=0.2,shuffle=True,epochs=5,verbose=1)

model.save('model.h5')

### Model evaluation performance
from keras.models import Model
import matplotlib.pyplot as plt

### plot the training and validation loss for each epoch
plt.plot(history_object.history['loss'])
plt.plot(history_object.history['val_loss'])
plt.title('model mean squared error loss')
plt.ylabel('mean squared error loss')
plt.xlabel('epoch')
plt.legend(['training set', 'validation set'], loc='upper right')
plt.savefig("Model Mean Square Error Loss Lake 3.png")
#plt.show()

exit()