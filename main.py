import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from moviepy.editor import VideoFileClip


from src import camera_calibration, process_image, find_lines, validation


def processImage(image):
    # undistort image
    undistort = process_image.undistort(image, calibrationFilePath)
    #plt.imshow(undistort, cmap='gray')
    #plt.savefig('output_images/undistort' + imageName)

    # draw lane lines
    laneLinesImage = process_image.drawPolygon(undistort)
    #plt.imshow(laneLinesImage, cmap='gray') 
    #plt.savefig('output_images/laneLines' + imageName)

    # process image color
    preprocessColor = process_image.preprocessColor(undistort)
    #plt.imshow(preprocessColor, cmap='gray')
    #plt.savefig('output_images/preprocess' + imageName)

    # change image perspective to a top-down view
    transformedImage = process_image.perspectiveTransform(preprocessColor, camera_calibration.xCorners, camera_calibration.yCorners)
    #plt.imshow(transformedImage, cmap='gray')
    #plt.savefig('output_images/transformed' + imageName)

    # detect lines
    if validationInstance.processFromScratch() is True:
        linesData = find_lines.fullSearch(transformedImage)
        validationInstance.setLeftFit(linesData['left_fit'])
        validationInstance.setRightFit(linesData['right_fit'])
    else:
        linesData = find_lines.searchFromFoundLines(transformedImage, validationInstance.getLeftFit(), validationInstance.getRightFit())

    """
    # plot detected lines
    find_lines.saveFileOfFoundLines(
        transformedImage,
        linesData['left_lane_inds'],
        linesData['right_lane_inds'],
        linesData['nonzerox'],
        linesData['nonzeroy'],
        linesData['ploty'],
        linesData['left_fitx'],
        linesData['right_fitx'],
        'output_images/lines' + imageName)
    """

    # lines curvature
    left_curvature, right_curvature = find_lines.getLinesCurvature(linesData['ploty'], linesData['left_fitx'], linesData['right_fitx'])
    distance_from_center = find_lines.getDistanceFromCenter(transformedImage.shape[1], linesData['left_fitx'], linesData['right_fitx'])

    # write log
    """
    print(' ')
    print('left', left_curvature)
    print('right', right_curvature)
    print('distance', distance_from_center)
    """

    validationInstance.validateImageResult(left_curvature, right_curvature)

    # output image
    return find_lines.drawResult(
        transformedImage,
        linesData['left_fitx'],
        linesData['right_fitx'],
        linesData['ploty'],
        process_image.getInversePerspectiveTransformMatrix(),
        undistort)


def runTest():
    # Import test images
    testImagesPath = 'test_images/'
    images = os.listdir(testImagesPath)
    for imageName in images:
        image = mpimg.imread(testImagesPath + imageName)
        plt.imshow(image, cmap='gray')
        plt.savefig('output_images/' + imageName)

        print(imageName)
        processImage(image)
        validationInstance.setnErrors(3)


def runVideo():
    output_file = './challenge_video_result.mp4'
    input_file = './challenge_video.mp4'
    print(os.path.isfile(input_file))
    clip = VideoFileClip(input_file)
    out_clip = clip.fl_image(processImage)
    out_clip.write_videofile(output_file, audio=False)


# calibrate camera
validationInstance = validation.Validation()
calibrationFilePath = camera_calibration.calibrate()
runVideo()
