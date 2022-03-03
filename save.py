from PIL import Image
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from astropy.io import fits
import numpy as np

song = 'https://open.spotify.com/track/7JdarpX08FLhmfNZpxqgUO?si=cca5b218096846ff'


def save(f):
    file = fits.open(f) 
    img_data = file[0].data
    print(img_data.shape)
    img_data = img_data[120:800, 320: 1110]
    norm = (img_data.astype(np.float)-img_data.min())*255.0 / (img_data.max()-img_data.min())
    Image.fromarray(norm.astype(np.uint8)).save('result.png') 

save('small_spider.fits')
