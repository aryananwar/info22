from astropy.io import fits
import csv

def gen(file_name):
    x = fits.open(file_name)
    hdr = x[0].header

    with open(hdr['DATE-OBS'] + '.csv', 'w') as file:
        writer = csv.writer(file, delimiter =' ', quoting=csv.QUOTE_ALL)
        writer.writerow(['FILE NAME', 'TIME-OBS', 'EXPTIME', 'PIXHEIGH', 'BZERO'])
        writer.writerow([file_name, hdr['TIME-OBS'], hdr['EXPTIME'], hdr['PIXHEIGH'], hdr['BZERO']])
            


gen('small_spider.fits')