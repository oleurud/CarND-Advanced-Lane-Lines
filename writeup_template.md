##Writeup Template
###You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./writeup_images/result-calibration2.jpg "Undistorted 1"
[image2]: ./writeup_images/result-calibration3.jpg "Undistorted 2"
[image3]: ./writeup_images/undistorttest3.jpg "Undistort test3"
[image4]: ./writeup_images/preprocesstest3.jpg "Preprocess test3"
[image5]: ./writeup_images/laneLinestest3.jpg "lane Lines test3"
[image6]: ./writeup_images/laneLinesTransformedtest3.jpg "lane Lines Transformed test3"
[image7]: ./writeup_images/transformedtest3.jpg "transformed test3"
[image8]: ./writeup_images/linestest3.jpg "lines test3"
[image9]: ./writeup_images/resulttest3.jpg "result test3"

[video1]: ./writeup_images/project_video_result.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points
Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
###Writeup / README

####1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  

You're reading it!

###Camera Calibration

####1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the file `camera_calibration.py`).  

I start by preparing `objectPoints`, which will be the (x, y, z) coordinates of the chessboard corners in the world and the `imagePoints` will be the 2D coordinates of the chessboard corners (Here I am assuming the chessboard is fixed on the (x, y) plane at z=0)

For each calibration image from `camera_cal` folder, find the chessboard corners using cv2.findChessboardCorners method. 

I then used the output `objectPoints` and `imagePoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` method and save the `mtx` and `dist` params in a file for future use of the calibration.

You can see the result of the `cv2.undistort()` method: 

Image undistort from calibration2.jpg
![alt text][image1] 

Image undistort from calibration3.jpg
![alt text][image2]

###Pipeline (single images)

You can follow the process pipeline in the method `processImage` of the file `main.py`

This main archive uses the files on src folder: `process_image.py`, `process_control.py` and `process_lines.py`

####1. Provide an example of a distortion-corrected image.

The first step is create the calibration camera file (line 135 of `main.py`).

This is the first stage of the `processImage` method who calls the method `undistort` of the file `process_image.py`. The method read the previous calibration file and calls the `cv2.undistort()` method.

To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this one:
![alt text][image3]

####2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

You can see the code of this step in the `preprocessColor` method of the `process_image.py` called in the line 37 of `main.py` file.

For the color, I tried to use RGB tranformations, using gray images or only the R channel. Finally I used the channel S of the HLS image.

I combined this channel S with the directional gradient, gradient magnitude and gradient direction of the image.

You can see the result:

![alt text][image4]

####3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

You can see the code of this step in the `perspectiveTransform` method of the `process_image.py` called in the line 43 of `main.py` file.

In this step, the more important thing is to find the perspective transform points in the images. You can see the results in the `getCornersOfView` method of the `process_image.py` which returns the source and destination points.

You can see the source points in this image:
![alt text][image5]

And the destination points in this image:
![alt text][image6]

With this points found, I used the `cv2.getPerspectiveTransform` and `cv2.warpPerspective` methods to transform the image to a top-down view. 

You can see the result after this steps:
![alt text][image7]


####4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

You can see the code of this step in the `process_lines.py` with is called in the `main.py` file (lines 50-53).

There are to 2 ways to find the lines:

- From the scratch (`fullSearch` method): look for the 2 places where the lines exist with more probability (histogram). Then, I used a sliding windows to find the lines in 9 steps. And finally, fit my lane lines with a 2nd order polynomial.

- Based on previous search (`searchFromFoundLines` method): when I have a good previous result, I dont need to find the lines from scratch again. Based on this previous result, I only look for the lines in near points of the previous results and do a 2nd order polynomial again.

Im both cases, the `processSeach` method calculates this 2nd order polynomial.

I used the ProcessControl class (`process_control.py`) for control the process:

- Validate one image result (`validateImageResult` method)
- Control if I need to start from scratch or not (`processFromScratch` method) controlling the number of errors of the last images
- And save the previous good results data


This is the result of this step:

![alt text][image8]

####5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

You can see the code of this step in the `getLinesCurvature` method of the `process_lines.py` called in the line 70 of `main.py` file.

Another similar step is the measurement of current distance from lane center of the vehicle. You can see the code in the `getDistanceFromCenter` method of the `process_lines.py` called in the line 71 of `main.py` file.

####6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

You can see the code of this step in the `drawResult` method of the `process_lines.py` called in the line 90 of `main.py` file.

I call to the cv2.warpPerspective again but using the inverse perspective transform matrix to get the real image again (undistort) and write the curvature and distance of the step before.

This is the result: 

![alt text][image9]

---

###Pipeline (video)

####1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video.mp4)

---

###Discussion

####1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

For sure, the more important step in the result of this project is the way to process the color transforms, gradients or other methods to create a thresholded binary image, because based on this preprocess I create the image to find the lines. For an improve result, is necessary to try using other channel of the image for diferent situations as low or high brightness, the color of the lines ... For example, this is the reason which my code not works well in the challenge video.

Another important thing is the time that I need to create the video: more than 5 minutes to get the lane colored video and the real video duration is 50 seconds. With this solution, it is impossible to create a real time app. In my code, the only way to improve time performance is increase the maxErrors var in the ProcessControl class (more errors to need a search from scratch with is slower), but in any case, this is not enougth. Another ways could be using anothe video libraries or process only some frames of the video (1 out of 5 for example, 1 each 200ms).