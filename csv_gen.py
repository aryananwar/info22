from astropy.io import fits
import csv

def gen(file_name):
    x = fits.open(file_name)
    hdr = x[0].header
# https://open.spotify.com/track/4cAgkb0ifwn0FSHGXnr4F6?si=e73fd5d7e49d405c
    with open(hdr['DATE-OBS'] + '.csv', 'w') as file:
        writer = csv.writer(file, delimiter =' ', quotechar='"',  quoting=csv.QUOTE_ALL )
        writer.writerow(['FILE NAME', 'TIME-OBS', 'EXPTIME', 'PIXHEIGH', 'BZERO'])
        writer.writerow([file_name, hdr['TIME-OBS'], hdr['EXPTIME'], hdr['PIXHEIGH'], hdr['BZERO']])
            


gen('small_spider.fits')