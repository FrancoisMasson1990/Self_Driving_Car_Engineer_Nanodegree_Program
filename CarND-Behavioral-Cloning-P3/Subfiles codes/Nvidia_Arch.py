# Documentation using Keras + explanation
# 
#### https://faroit.github.io/keras-docs/1.0.1/
#
# Implementation of NVIDIA Architecture
# https://devblogs.nvidia.com/deep-learning-self-driving-cars/


from keras.models import Sequential
from keras.layers import Flatten,Dense, Lambda
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D

model = Sequential()
model.add(Lambda(lambda x: x /255.0 -0.5, input_shape=(160,320,3)))
#The example below crops:
#75 rows pixels from the top of the image
#25 rows pixels from the bottom of the image
#0 columns of pixels from the left of the image
#0 columns of pixels from the right of the image
model.add(Cropping2D(cropping=((75,25), (0,0))))
model.add(Convolution2D(24,5,5,subsample=(2,2),activation="relu"))
model.add(Convolution2D(36,5,5,subsample=(2,2),activation="relu"))
model.add(Convolution2D(48,5,5,subsample=(2,2),activation="relu"))
model.add(Convolution2D(64,3,3,activation="relu"))
model.add(Convolution2D(64,3,3,activation="relu"))
model.add(Flatten())
model.add(Dense(100))
model.add(Dense(50))
model.add(Dense(10))
model.add(Dense(1))

model.compile(loss='mse',optimizer='adam')
history_object = model.fit(X_train,y_train,validation_split=0.2,shuffle=True,epochs=5,verbose=1)

model.save('model.h5')