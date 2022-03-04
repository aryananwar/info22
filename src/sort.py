from astropy.io import fits
import os
import csv
import datetime
dates = {}


class Sort:
    def organize(self):
        for file in os.listdir('fits'):
            filename = file
            if 'tmp' not in file and '.fits' in file:
                if file == '.DS_Store':
                    continue
                file = fits.open(f"./fits/{file}")
                date = file[0].header['DATE-OBS'].split('T')[0]
                if date not in os.listdir('fits'):
                    try:
                        os.mkdir(f"./fits/{date}")
                    except Exception as e:
                        print(e)
                        pass
                    os.rename(f"./fits/{filename}", f"./fits/{date}/{file[0].header['DATE-OBS']}.fits")
                else:   
                    os.rename(f"./fits/{filename}", f"./fits/{date}/{file[0].header['DATE-OBS']}.fits")
        return 'Files have been organized.'
    def getData(self):
        a = ''
        for directory in os.listdir('./fits'):
            if os.path.isdir(f"fits/{directory}"):
                print(directory)
                for file in os.listdir(f"fits/{directory}"):
                    filename = file
                    if 'tmp' not in file and '.fits' in file:
                        if file == '.DS_Store':
                            continue          
                        file = fits.open(f"./fits/{directory}/{file}")
                        date = file[0].header['DATE-OBS'].split('T')[0]
                        a += file[0].header['DATE-OBS'] + '\n'
                        bugs = 0
                        if file[0].header['hasBug']:
                            bugs = 1
                        if date not in dates:
                            dates[date] = {
                                "pictures": 1,
                                "telescopeUsed": file[0].header['TELESCOP'],
                                "location": file[0].header['OBSERVER'],
                                "instrument": file[0].header['INSTRUME'],
                                "dates": [file[0].header['DATE-OBS']],
                                "bugs": bugs
                            }
                        else:
                            dates[date]['pictures'] += 1
                            dates[date]['dates'].append(file[0].header['DATE-OBS'])
                            dates[date]['bugs'] += bugs
                            if(dates[date]['telescopeUsed'] != file[0].header['TELESCOP']):
                                print('telescope mismatch')
                            if(dates[date]['instrument'] != file[0].header['INSTRUME']):
                                print('Instrument mismatch')



        for date, value in dates.items():
            lowestTime = {"value": 24, "string": None}
            highestTime = {"value": 0, "string": None}
            for iso in value['dates']:
                time = iso.split('T')[1].split('-')
                hour = time[0]
                minute = time[1]
                second = time[2]
                time = int(hour) + int(minute)/60 + float(second)/3600
                if time > highestTime['value']:
                    highestTime['string'] = f"{hour}:{minute}:{second}"
                    highestTime['value'] = time
                elif time < lowestTime['value']:
                    lowestTime['string'] = f"{hour}:{minute}:{second}"
                    lowestTime['value'] = time
            dates[date]['lowestTime'] = lowestTime
            dates[date]['highestTime'] = highestTime
            del dates[date]['dates']

        return dates
    
    def csvGen(self):
        with open('data' + '.csv', 'w') as file:
            writer = csv.writer(file, delimiter =',', quotechar='"',  quoting=csv.QUOTE_ALL)
            writer.writerow(['FILE NAME', 'DATE', 'TIME', 'EXPTIME', 'LOCATION', 'INSTRUMENT'])
            for directory in os.listdir('../fits'):
                if os.path.isdir(f"../fits/{directory}"):
                    print(directory)
                    for file in os.listdir(f"../fits/{directory}"):
                        filename = file
                        if 'tmp' not in file and '.fits' in file:
                            if file == '.DS_Store':
                                continue          
                            file = fits.open(f"../fits/{directory}/{file}")
                            hdr = file[0].header
                            writer.writerow([filename, hdr['DATE-OBS'].split('T')[0], hdr['DATE-OBS'].split('T')[1], hdr['EXPTIME'], hdr['OBSERVER'], hdr['INSTRUME']])
    


a = Sort()
a.csvGen()