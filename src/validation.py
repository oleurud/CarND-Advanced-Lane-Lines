"""
Based on lesson 35
"""
import numpy as np


class Validation:
    def __init__(self):
        # max errors
        self.maxErrors = 3
        # current errors. Starts in the maximun to force the full search for the first image
        self.nErrors = self.maxErrors

        self.left_fit = np.zeros(3)
        self.right_fit = np.zeros(3)


    def validateImageResult(self, left_curvature, right_curvature):
        curvatureDifferential = 7.5
        if left_curvature * curvatureDifferential < right_curvature or left_curvature > right_curvature * curvatureDifferential:
            self.nErrors = self.nErrors + 1
        else:
            self.nErrors = 0


    def processFromScratch(self):
        if self.nErrors >= self.maxErrors:
            self.nErrors = 0
            return True
        else:
            return False


    def setnErrors(self, nErrors):
        self.nErrors = nErrors

    def getLeftFit(self):
        return self.left_fit

    def setLeftFit(self, left_fit):
        self.left_fit = left_fit

    def getRightFit(self):
        return self.right_fit

    def setRightFit(self, right_fit):
        self.right_fit = right_fit
