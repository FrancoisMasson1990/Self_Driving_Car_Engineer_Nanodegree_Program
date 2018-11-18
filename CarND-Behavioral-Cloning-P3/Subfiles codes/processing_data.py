#Preprocessing the data is done most of the time in two step 
# Normalizing the data and mean centering the data 

#Lambda Layers
#In Keras, lambda layers can be used to create arbitrary functions that operate on each image as it passes through the layer.

#In this project, a lambda layer is a convenient way to parallelize image normalization. The lambda layer will also ensure that the model will normalize input images when making predictions in drive.py.

#That lambda layer could take each pixel in an image and run it through the formulas:
#pixel_normalized = pixel / 255
#pixel_mean_centered = pixel_normalized - 0.5

#A lambda layer will look something like: Lambda(lambda x: (x / 255.0) - 0.5)

X_train = np.array(images)
y_train = np.array(measurements)

from keras.models import Sequential
from keras.layers import Flatten,Dense, Lambda # Import Lambda for normalization in parallel

model = Sequential()
model.add(Lambda(lambda x: x /255.0 -0.5, input_shape=(160,320,3)))
model.add(Flatten())
model.add(Dense(1))

model.compile(loss='mse',optimizer='adam')
model.fit(X_train,y_train,validation_split=0.2,shuffle=True)

model.save('model.h5')
exit()