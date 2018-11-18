#Flipping Images And Steering Measurements
#A effective technique for helping with the left turn bias involves flipping images and taking the opposite sign of the steering measurement. For example:

augmented_images, augmented_measurements=[],[]
for image,measurement in zip(images,measurements):
    augmented_images.append(image)
    augmented_measurement.append(measurement)
    augmented_images.append(cv2.flip(image,1))
    augmented_measurement.append(measurement*-1)