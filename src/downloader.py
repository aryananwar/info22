# Import Libraries
import wget
import os

class downloader:
    def downloadFits():
        # Check to see if output directory exists
        if os.path.isdir('./fits') == False:
            # If the output directory does not exist, create it
            print('[*] Creating output directory "fits"...')
            os.mkdir('./fits')

        # Download FITS images
        print("[!] Downloading all FITS images...")
        for listname in os.listdir("../allsky_file_list"):
            with open(os.path.join("../allsky_file_list", listname), 'r') as f:
                contents = f.read().split("\n")
                for fit in contents:
                    try:
                        wget.download("https://mdallsky.astro.umd.edu/masn01-archive/" + fit[2:6] + fit[1:], out="fits/" + fit.split("/")[3]) # Parse each line and structure a valid url to wget
                    except Exception as e:
                        print(e)
        return
