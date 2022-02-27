# Import libraries
import wget
import os

# Open the folder containing lists of all fits locations
print("Downloading all fits")

for listname in os.listdir("allsky_file_list"):
    with open(os.path.join("allsky_file_list", listname), 'r') as f:
        contents = f.read().split("\n")
        for fit in contents:
            try:
                wget.download("https://mdallsky.astro.umd.edu/masn01-archive/" + fit[2:6] + fit[1:], out="fits/" + fit.split("/")[3]) # Parse each line and structure a valid url to wget
            except:
                print("Caught invalid url")
