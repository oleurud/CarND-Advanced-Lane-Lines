"""
Based on lessons 11, 17, 28, 29
"""

import pickle
import cv2
import numpy as np

def preprocessColor(image):
    """
    Returns processed image color
    Process:
        - Get the image binary of the channel S of the HLS image 
        - Get the combined threshold of directional gradient, gradient magnitude and gradient direction
        - Combined both
    """
    #return preprocessColorGray(image)
    #return preprocessColorR(image)
    #return preprocessColorS(image)
    #return preprocessColorThreshold(image)

    S = preprocessColorS(image)
    threshold = preprocessColorThreshold(image)
    
    combined_binary = np.zeros_like(S)
    combined_binary[(threshold == 1) | (S == 1)] = 1
    
    return combined_binary


def preprocessColorGray(image):
    """
    Returns the binary of the gray image
    """
    thresh = (180, 255)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    binary = np.zeros_like(gray)
    binary[(gray > thresh[0]) & (gray <= thresh[1])] = 1
    return binary

def preprocessColorR(image):
    """
    Returns the binary of the channel R of the RGB image
    """
    R = image[:,:,0]
    thresh = (200, 255)
    binary = np.zeros_like(R)
    binary[(R > thresh[0]) & (R <= thresh[1])] = 1
    return binary    

def preprocessColorS(image):
    """
    Returns the binary of the channel S of the HLS image
    """
    hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
    S = hls[:,:,2]
    thresh = (90, 255)
    binary = np.zeros_like(S)
    binary[(S > thresh[0]) & (S <= thresh[1])] = 1
    return binary


def preprocessColorThreshold(image):
    """
    Returns the combined threshold of directional gradient, gradient magnitude and gradient direction
    """

    ksize = 3

    gradx = abs_sobel_thresh(image, orient='x', thresh_min=20, thresh_max=100)
    mag_binary = mag_thresh(image, sobel_kernel=ksize, mag_thresh=(30, 100))
    dir_binary = dir_threshold(image, sobel_kernel=ksize, thresh=(0.7, 1.3))

    combined = np.zeros_like(dir_binary)
    combined[(gradx == 1) | ((mag_binary == 1) & (dir_binary == 1))] = 1
    return combined


def abs_sobel_thresh(image, orient='x', sobel_kernel=3, thresh_min=0, thresh_max=255):
    """
    Returns binary directional gradient of image
    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    if orient == 'x':
        abs_sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 1, 0))
    if orient == 'y':
        abs_sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 0, 1))
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
    sxbinary = np.zeros_like(scaled_sobel)
    sxbinary[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1
    
    return sxbinary

def mag_thresh(image, sobel_kernel=3, mag_thresh=(0, 255)):
    """
    Returns binary gradient magnitude of image
    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    gradmag = np.sqrt(sobelx**2 + sobely**2)
    scale_factor = np.max(gradmag)/255 
    gradmag = (gradmag/scale_factor).astype(np.uint8) 
    binary_output = np.zeros_like(gradmag)
    binary_output[(gradmag >= mag_thresh[0]) & (gradmag <= mag_thresh[1])] = 1

    return binary_output
    
def dir_threshold(image, sobel_kernel=3, thresh=(0, np.pi/2)):
    """
    Returns binary gradient direction of image
    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    absgraddir = np.arctan2(np.absolute(sobely), np.absolute(sobelx))
    binary_output =  np.zeros_like(absgraddir)
    binary_output[(absgraddir >= thresh[0]) & (absgraddir <= thresh[1])] = 1

    return binary_output


def drawPolygon(image):
    #draw the lines in a new image
    image = np.copy(image)
    
    corners = np.int32(getCornersOfView())
    corners = corners.reshape((-1,1,2))

    cv2.polylines(image, [corners], True, (255,0,0), 2)

    return image


def undistort(image, calibrationFilePath):
    """
    undistort image based in camera_calibration
    """

    calibrationData = pickle.load( open(calibrationFilePath, "rb") )
    return cv2.undistort(image, calibrationData['mtx'], calibrationData['dist'], None, calibrationData['mtx'])


def perspectiveTransform(undistortImage, xCorners, yCorners):
    """
    returns image to a top-down view
    """

    M = getPerspectiveTransformMatrix()
    img_size = (undistortImage.shape[1], undistortImage.shape[0])
    return cv2.warpPerspective(undistortImage, M, img_size)


def getPerspectiveTransformMatrix():
    """
    Returns the perspective transform matrix for perspectiveTransform
    """

    corners = np.float32(getCornersOfView())
    new_top_left = np.array([corners[0, 0], 0])
    new_top_right = np.array([corners[3, 0], 0])
    offset = [50, 0]

    src = np.float32([corners[0], corners[1], corners[2], corners[3]])
    dst = np.float32([corners[0] + offset, new_top_left + offset, new_top_right - offset, corners[3] - offset])

    return cv2.getPerspectiveTransform(src, dst)


def getCornersOfView():
    return [[253, 697], [585, 456], [700, 456], [1061, 690]]