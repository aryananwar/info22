# Import utils
from src.downloader import downloader
from src.converter import converter

class umdInfo:
    def getQuery(self):
        response = input(
            """
[!] Select What you would like to do
1) Download FITS images
2) Convert FITS images to JPGs
3) Analyze JPGs
4) Close Tool

=> """
        )

        # Handle input
        match response:
            case "1":
                print("[*] You selected: Download FITS images")
                handler = downloader.downloadFits()
                print("[!] Finished downloading FITS files")
                return self.getQuery()
            case "2":
                print("[*] You selected: Convert FITS images to JPGs")
                handler = converter.convertFITS()
                print("[!] Finished converting FITS files")
                return self.getQuery()
            case "3":
                print("[*] You selected: Analyze JPGs")
            case "4": 
                quit()
            case _:
                print("[!] Please enter one of the options!")
                return self.getQuery()

instance = umdInfo()
instance.getQuery()