import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import astropy_mpl_style



def loads(f):
    plt.style.use(astropy_mpl_style)
    file = fits.open(f) 
    img_data = file[0].data
    plt.figure()
    
    plt.imshow(img_data, cmap ="gray")
    plt.colorbar()
    plt.show()


loads('small_spider.fits')
