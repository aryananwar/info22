from matplotlib import use
import matplotlib.pyplot as plt
from astropy.io import fits
import os

from numpy import true_divide

class View:
    def view_multiple():
        folder = './fits'
        useDefault = input('Use Default Path? (./fits/) (y/n)\n')
        if useDefault == 'y' or useDefault == 'Y':
            useDefault = True
        else:
            useDefault = False
        if not useDefault:
            folder = input('Enter path to fits folder')
        for directory in os.listdir(folder):
            if directory == 'out':
                continue
            if os.path.isdir(f"{folder}/{directory}"):
                for f in os.listdir(f"{folder}/{directory}"):
                    if 'tmp' in f:
                        continue
                    try:
                        yo = fits.open(f"{folder}/{directory}/{f}") 
                        img_data = yo[0].data 
                        plt.figure()
                        plt.imshow(img_data, cmap ="gray")
                        plt.colorbar()
                        plt.show()
                    except FileNotFoundError as e:
                        print(e)
                        pass

