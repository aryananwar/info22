# Import necessary libraries
import cv2 as cv
import numpy as np
import os
from astropy.io import fits

class obstructionDetector:
    def obstructionDetector():
        print("[!] Analyzing JPGs")
        for jpg in os.listdir("./JPGs"):
            try:
                # Load image
                img = cv.imread("./JPGs/" + jpg)

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

                print("[*] Number of obstructions detected in " + jpg + ": " + str(len(keypoints)))
                filename = jpg.split('.jpg')[0]
                file = fits.open(f"./fits/{filename.split('T')[0]}/{filename}", mode='update')
                print(file[0].header)
                file[0].header.set('bugs', len(keypoints))
                file.close()
            except Exception as e:
                print(e)
                pass