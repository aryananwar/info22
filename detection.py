import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from astropy.io import fits
from astropy.visualization import astropy_mpl_style
from loading.py import loads

#open fits file
loads()
#adjust contrast and shadows/highlights


#opening image and adding contours
img = cv.imread('img.jpg')
imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, 0)
im2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
data = cv.drawContours(img, contours, -1, (0,255,0), 3)

#display image for debugging
plt.imshow(data, interpolation='nearest')
plt.show()
