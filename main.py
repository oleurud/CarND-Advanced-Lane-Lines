import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from src import camera_calibration, process_image, find_lines


def processImage(image, imageName, detected = False):
    # undistort image
    undistort = process_image.undistort(image, calibrationFilePath)
    plt.imshow(undistort, cmap='gray')
    plt.savefig('output_images/undistort' + imageName)

    # draw lane lines
    laneLinesImage = process_image.drawPolygon(undistort)
    plt.imshow(laneLinesImage, cmap='gray')
    plt.savefig('output_images/laneLines' + imageName)

    # process image color
    preprocessColor = process_image.preprocessColor(undistort)
    plt.imshow(preprocessColor, cmap='gray')
    plt.savefig('output_images/preprocess' + imageName)

    # change image perspective to a top-down view
    transformedImage = process_image.perspectiveTransform(preprocessColor, camera_calibration.xCorners, camera_calibration.yCorners)
    plt.imshow(transformedImage, cmap='gray')
    plt.savefig('output_images/transformed' + imageName)

    # detect lines
    if detected is False:
        left_lane_inds, right_lane_inds, left_fit, right_fit, nonzerox, nonzeroy = find_lines.fullSearch(transformedImage)
        find_lines.saveFileOfFoundLines(transformedImage, left_lane_inds, right_lane_inds, left_fit, right_fit, nonzerox, nonzeroy, 'output_images/lines' + imageName)
    else:
        left_lane_inds, right_lane_inds, left_fit, right_fit, nonzerox, nonzeroy = find_lines.searchFromFoundLines(transformedImage2, left_fit, right_fit)
        find_lines.saveFileOfFoundLines(transformedImage, left_lane_inds, right_lane_inds, left_fit, right_fit, nonzerox, nonzeroy, 'output_images/lines' + imageName)


# calibrate camera
calibrationFilePath = camera_calibration.calibrate()

# Import test images
testImagesPath = 'test_images/'
images = os.listdir(testImagesPath)
for imageName in images:
    image = mpimg.imread(testImagesPath + imageName)
    plt.imshow(image, cmap='gray')
    plt.savefig('output_images/' + imageName)

    processImage(image, imageName)
