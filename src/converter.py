# Import Libraries
from PIL import Image
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from astropy.io import fits
import numpy as np
import os

class converter:
    def convertFITS():
        # Check to see if output directory exists
        if os.path.isdir('../JPGs') == False:
            # If the output directory does not exist, create it
            print('[*] Creating output directory "JPGs"...')
            os.mkdir('../JPGs')

        print("[!] Converting all FITS to JPGs")
        for fitsFile in os.listdir("./fits"):
            print(fitsFile)
            if "tmp" in str(fitsFile):
                pass
            else:
                try:
                    file = fits.open(os.path.join("./fits", fitsFile))
                    img_data = file[0].data
                    img_data = img_data[240:750, 350:1100]
                    norm = (img_data.astype(np.float)-img_data.min())*255.0 / (img_data.max()-img_data.min())
                    Image.fromarray(norm.astype(np.uint8)).save(os.path.join("../JPGs", fitsFile) + ".jpg")
                    print("[*] Converted: " + fitsFile)
                except:
                    pass