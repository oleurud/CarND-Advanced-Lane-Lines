import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle

from src import camera_calibration, process_image, find_lines


# calibrate camera
calibrationFilePath = camera_calibration.calibrate()

# test image
#straight_lines2
image = mpimg.imread('test_images/test3.jpg')
plt.imshow(image, cmap='gray')
plt.savefig('output_images/image.jpg')

# undistort image
undistort = process_image.undistort(image, calibrationFilePath)
plt.imshow(undistort, cmap='gray')
plt.savefig('output_images/undistortImage.jpg')

# draw lane lines
"""
laneLinesImage = process_image.drawPolygon(undistort)
plt.imshow(laneLinesImage, cmap='gray')
plt.savefig('output_images/laneLinesImage.jpg')
"""

# process image color
preprocessColor = process_image.preprocessColor(undistort)
plt.imshow(preprocessColor, cmap='gray')
plt.savefig('output_images/preprocessImage.jpg')

# change image perspective to a top-down view
transformedImage = process_image.perspectiveTransform(preprocessColor, camera_calibration.xCorners, camera_calibration.yCorners)
plt.imshow(transformedImage, cmap='gray')
plt.savefig('output_images/transformedImage.jpg')


# detect lines
out_img, ploty, left_fitx, right_fitx = find_lines.findingLines(transformedImage)
plt.imshow(out_img)
plt.plot(left_fitx, ploty, color='yellow')
plt.plot(right_fitx, ploty, color='yellow')
plt.xlim(0, 1280)
plt.ylim(720, 0)
plt.savefig('output_images/linesImage.jpg')