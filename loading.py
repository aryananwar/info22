import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import astropy_mpl_style

hdu = fits.PrimaryHDU()

def loads(f):
    plt.style.use(astropy_mpl_style)
    file = fits.open(f) 

    arr = file[0].data
    for i in file:
        arr+= file[i].data
    return arr

    plt.figure()
    plt.imshow(img_data, cmap ="gray")
    plt.colorbar()
    plt.show()

x = loads('small spider.fits')
hdu.header
