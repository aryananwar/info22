# Import necessary libraries
import cv2 as cv
import numpy as np

# Load image
img = cv.imread("result.jpg")

# Apply a median filter to remove noise
median = cv.medianBlur(img, 5)

# Step 2----------------------------------------------------------------------------------
# Convert image to RGB and create a 2D array of color values
image = cv.cvtColor(median, cv.COLOR_BGR2RGB)
pixels = image.reshape((-1, 3))
pixels = np.float32(pixels)

# Save time of kmeans segmentation by specifying a limit on iterations
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.1)

# Create color clusters
k = 9
_, labels, (centers) = cv.kmeans(pixels, k, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)

# convert back to 8 bit values
centers = np.uint8(centers)
labels = labels.flatten()

# convert all pixels to the color of the centroids
segmented_image = centers[labels.flatten()]
segmented_image = segmented_image.reshape(image.shape)

# Step 3----------------------------------------------------------------------------------
# Setup SimpleBlobDetector parameters.
params = cv.SimpleBlobDetector_Params()

params.minThreshold = 75;
params.maxThreshold = 100;
params.filterByArea = True
params.minArea = 40
params.filterByCircularity = True
params.minCircularity = 0.1
params.filterByConvexity = True
params.minConvexity = 0.87
params.filterByInertia = True
params.minInertiaRatio = 0.01

detector = cv.SimpleBlobDetector_create(params)
keypoints = detector.detect(segmented_image)

result = cv.drawKeypoints(segmented_image, keypoints, np.array([]), (0,0,255), cv.DrawMatchesFlags_DRAW_RICH_KEYPOINTS)

print("Number of obstructions detected: " + str(len(keypoints)))

# Display results
compare = np.concatenate((img, result), axis=1)
cv.imshow("Sample", compare)
cv.waitKey(0)