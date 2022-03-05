# Import necessary libraries
import cv2 as cv
import numpy as np
import os
from astropy.io import fits
from PIL import Image

class obstructionDetector:
    def obstructionDetector():
        for directory in os.listdir('./fits'):
            print("[!] Analyzing FITS files in: " + str(directory))
            if os.path.isdir(f"./fits/{directory}"):
                for sample in os.listdir(f"fits/{directory}"):
                    if "tmp" in str(sample):
                        pass
                    else:
                        try:
                            # Crop and save image as JPGs
                            file = fits.open(os.path.join(f"./fits/{directory}", sample))
                            img_data = file[0].data
                            img_data = img_data[240:700, 350:1100]
                            norm = (img_data.astype(np.float)-img_data.min())*255.0 / (img_data.max()-img_data.min())
                            Image.fromarray(norm.astype(np.uint8)).save(os.path.join("./tmp") + ".jpg")
                            print("[*] Processing: " + sample)

                            try:
                                # Load image
                                img = cv.imread("./tmp.jpg")

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
                                k = 8
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

                                params.minThreshold = 30
                                params.maxThreshold = 255
                                params.filterByArea = True
                                params.minArea = 30
                                params.filterByCircularity = True
                                params.minCircularity = 0.1
                                params.filterByConvexity = True
                                params.minConvexity = 0.2
                                params.filterByInertia = True
                                params.minInertiaRatio = 0.1

                                detector = cv.SimpleBlobDetector_create(params)
                                keypoints = detector.detect(segmented_image)

                                # Export result
                                result = cv.drawKeypoints(segmented_image, keypoints, np.array([]), (0,0,255), cv.DrawMatchesFlags_DRAW_RICH_KEYPOINTS)
                                if os.path.isdir('./fits/out') == False:
                                    # If the output directory does not exist, create it
                                    print('[*] Creating output directory "fits/out"...')
                                    os.mkdir('./fits/out')
                                cv.imwrite("./fits/out/" + sample + ".jpg", result)

                                print("[*] Number of obstructions detected in " + sample + ": " + str(len(keypoints)))
                                filename = sample.split('.jpg')[0]
                                file = fits.open(f"./fits/{filename.split('T')[0]}/{filename}", mode='update')
                                file[0].header.set('bugs', len(keypoints))
                                file.close()
                            except Exception as e:
                                pass
                        except Exception as e:
                            print(e)