# Import libraries
import wget
import os
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits
astropy_mpl_style['axes.grid'] = False
plt.style.use(astropy_mpl_style)

def init():
    downloadChoice = input("Would you like to download all fits files? (y/n): ")
    if downloadChoice.capitalize() == "Y":
        downloadFits()
    else:
        anaylizeTest()

# Open the folder containing lists of all fits locations
def downloadFits():
    print("Downloading all fits")
    for listname in os.listdir("allsky_file_list"):
        with open(os.path.join("allsky_file_list", listname), 'r') as f:
            contents = f.read().split("\n")
            for fit in contents:
                try:
                    wget.download("https://mdallsky.astro.umd.edu/masn01-archive/" + fit[2:6] + fit[1:], out="fits/" + fit.split("/")[3]) # Parse each line and structure a valid url to wget
                except Exception as e:
                    print(e)

def anaylizeTest():
    image_file = get_pkg_data_filename('MASN01-2015-06-19T23-43-22.fits')
    image_data = fits.getdata(image_file, ext=0)
    print(image_data)
    print(fits.info(image_file))
    plt.figure()
    plt.imshow(image_data, cmap="gray")
    plt.colorbar()
    plt.show()


init()