# Import utils
from src.downloader import downloader
from src.converter import converter
from src.obstructionDetector import obstructionDetector
from src.view import View
from src.sort import Sort
from colorama import Fore

class umdInfo:
    def getQuery(self):
        response = input(Fore.MAGENTA +
            """
[!] Select What you would like to do
1) Download FITS images
2) Analyze FITS Images
3) Export Results
4) View FITS
5) Close Tool

=> """
        )

        # Handle input
        match response:
            case "1":
                print(Fore.CYAN + "[*] You selected: Download FITS images")
                handler = downloader.downloadFits()
                print(Fore.CYAN + '\n[!] Sorting files')
                a = Sort()
                a.organize()
                print(Fore.GREEN + "[!] Finished downloading FITS files")
                return self.getQuery()
            case "2":
                print(Fore.CYAN + "[*] You selected: Analyze FITS Images")
                handler = obstructionDetector.obstructionDetector()
                print(Fore.GREEN + "[!] Finished analyzing FITS files")
                return self.getQuery()
            case "3":
                print(Fore.CYAN + "[*] You selected: Export Results")
                a.csvGen()
                a.getData()
                print(Fore.GREEN + '[!] Finished Exporting results as "data.csv"')
                return self.getQuery()
            case "4":
                print(Fore.CYAN + "[*] You selected: View FITS")
                View.view_multiple()
                return self.getQuery()
            case "5": 
                print(Fore.GREEN + '[!] Thank you! Have a good day.')
                quit()
            case _:
                print("[!] Please enter one of the options!")
                return self.getQuery()

instance = umdInfo()
instance.getQuery()