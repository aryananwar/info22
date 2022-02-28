# Import libraries
import wget
import os

def init():
    downloadChoice = input("Would you like to download all fits files? (y/n): ")
    if downloadChoice.capitalize() == "Y":
        downloadFits()
    else:
        print("Analyzing images")

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

init()