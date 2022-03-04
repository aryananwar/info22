import matplotlib.pyplot as plt
from astropy.io import fits
import os


class View:
    def view_one(f):
        file = fits.open(f) 
        img_data = file[0].data
        plt.figure()
            
        plt.imshow(img_data, cmap ="gray")
        plt.colorbar()
        plt.show()

    def view_multiple():
        folder = input('Enter path to fits folder: ')
        for f in os.listdir(folder):
            try:
                file = fits.open(f) 
                img_data = file[0].data
            except:
                pass
            
        x = ' '    
        while(x != '0'):
            plt.figure()
            plt.imshow(img_data, cmap ="gray")
            plt.colorbar()
            plt.show()

            print('Press any key to view next file.')
            x = input()