import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle

from src import camera_calibration, process_image


# calibrate camera
calibrationFilePath = camera_calibration.calibrate()

# test image
image = mpimg.imread('test_images/test5.jpg')
plt.imshow(image, cmap='gray')
plt.savefig('output_images/image.jpg')

# undistort image
undistort = process_image.undistort(image, calibrationFilePath)
plt.imshow(undistort, cmap='gray')
plt.savefig('output_images/undistortImage.jpg')

# preprocessColor
preprocessColor = process_image.preprocessColor(undistort)
plt.imshow(preprocessColor, cmap='gray')
plt.savefig('output_images/preprocessImage.jpg')

# image perspective transform to a top-down view
transformedImage = process_image.perspectiveTransform(preprocessColor, camera_calibration.xCorners, camera_calibration.yCorners)
plt.imshow(transformedImage, cmap='gray')
plt.savefig('output_images/transformedImage.jpg')


