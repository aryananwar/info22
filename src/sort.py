from astropy.io import fits
import os
import csv
import datetime
import json
dates = {}

class Sort:
    def __init__(self):
        with open('./data.json', 'r') as f:
            self.weather = json.load(f)
    def organize(self):
        print('Organizing All FITS Files Now')
        for file in os.listdir('./fits'):
            if 'out' in file:
                continue
            try:
                filename = file
                if 'tmp' not in file and '.fits' in file:
                    if file == '.DS_Store':
                        continue
                    file = fits.open(f"./fits/{file}")
                    file.close()
                    date = file[0].header['DATE-OBS'].split('T')[0]
                    if 'TIME-OBS' in file[0].header:
                        time = 'T' + file[0].header['TIME-OBS'].replace(':', '-')
                    else:
                        time = ''
                    if date not in os.listdir('./fits'):
                        try:
                            os.mkdir(f"./fits/{date}")
                        except Exception as e:
                            print(e)
                            pass
                        os.rename(f"./fits/{filename}", f"./fits/{date}/{file[0].header['DATE-OBS']}{time}".replace(':', '-') + ".fits")
                    else:   
                        os.rename(f"./fits/{filename}", f"./fits/{date}/{file[0].header['DATE-OBS']}{time}".replace(':', '-') + ".fits")
            except Exception as e:
                print("Error handling " + str(file) + ": " + str(e))
        return 'Files have been organized.'

    def getData(self):
        a = ''
        for directory in os.listdir('./fits'):
            if directory == 'out':
                continue
            try:
                if os.path.isdir(f"./fits/{directory}"):
                    for file in os.listdir(f"./fits/{directory}"):
                        filename = file
                        if 'tmp' not in file and '.fits' in file:
                            if file == '.DS_Store':
                                continue          
                            file = fits.open(f"./fits/{directory}/{file}")
                            date = file[0].header['DATE-OBS'].split('T')[0]
                            a += file[0].header['DATE-OBS'] + '\n'
                            bugs = 0
                            if file[0].header['bugs']:
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
                                if 'bugs' in dates[date]:
                                    dates[date]['bugs'] += bugs
                                else:
                                    dates[date]['bugs'] = bugs
                                if(dates[date]['telescopeUsed'] != file[0].header['TELESCOP']):
                                    print('telescope mismatch')
                                if(dates[date]['instrument'] != file[0].header['INSTRUME']):
                                    print('Instrument mismatch')
                            if 'TIME-OBS' in file[0].header:
                                dates[date]['time'] = file[0].header['TIME-OBS'].replace(':', '-')
                            else:
                                dates[date]['time'] = None
            except Exception as e:
                print("Error handling directory" + str(directory) + ": " + str(e))

        for date, value in dates.items():
            lowestTime = {"value": 24, "string": None}
            highestTime = {"value": 0, "string": None}
            for iso in value['dates']:
                if not value['time']: 
                    if ':' in iso:
                        time = iso.split('T')[1].split(':')
                    else:
                        time = iso.split('T')[1].split('-')
                else:
                    if ':' in value['time']:
                        time = value['item'].split(':')
                    else:
                        time = value['time'].split('-')
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

        for date, value in dates.items():
            with open(f"./fits/{date}/metadata.json", 'w') as f:
                json.dump(value, f)

        return dates
    
    def csvGen(self):
        try:
            with open('data' + '.csv', 'w') as file:
                writer = csv.writer(file, delimiter =',', quotechar='"',  quoting=csv.QUOTE_ALL)
                writer.writerow(['FILE NAME', 'DATE', 'TIME', 'DAY/NIGHT', 'EXPTIME', 'LOCATION', 'INSTRUMENT', 'BUGS', 'UNIX', 'TEMP', 'CLOUD %', 'VISIBILITY', 'INFO'])
                for directory in os.listdir('./fits'):
                    if directory == 'out':
                        continue
                    if os.path.isdir(f"./fits/{directory}"):
                        for file in os.listdir(f"./fits/{directory}"):
                            if file == 'metadata.json':
                                continue
                            filename = file
                            if 'tmp' not in file and '.fits' in file:
                                if file == '.DS_Store':
                                    continue
                                file = fits.open(f"./fits/{directory}/{file}")
                                hdr = file[0].header
                                if('TIME-OBS' in file[0].header):
                                    time = file[0].header['TIME-OBS'].replace('-', ':')
                                    date = file[0].header['DATE-OBS'].replace(':', '-')
                                    dayNight = 0
                                    timeSplit = time.split(':')
                                    if 7 <= int(timeSplit[0]) <= 19:
                                        dayNight = 'Day'
                                    else:
                                        dayNight = 'Night'
                                    
                                    isots = datetime.datetime.strptime(f"{date}T{time}", '%Y-%m-%dT%H:%M:%S')
                                    unix = (isots - datetime.datetime(1970, 1, 1)).total_seconds()
                                    unix = int(unix//3600 * 3600)
                                else:
                                    time = file[0].header['DATE-OBS'].split('T')[1].replace(':', '-')
                                    dayNight = 0
                                    timeSplit = time.split('-')
                                    if 7 <= int(timeSplit[0]) <= 19:
                                        dayNight = 'Day'
                                    else:
                                        dayNight = 'Night'
                                    date = file[0].header['DATE-OBS'].split('T')[0].replace(':', '-')
                                    isots = datetime.datetime.strptime(f"{date}T{time}", '%Y-%m-%dT%H-%M-%S.%f')
                                    unix = (isots - datetime.datetime(1970, 1, 1)).total_seconds()
                                    unix = int(unix//3600 * 3600)
                                for item in self.weather:
                                    if item['dt'] == unix:
                                        temp = item
                                        break
                                if 'BUGS' in hdr:
                                    bugs = hdr['BUGS']
                                else:
                                    bugs = 0
                                writer.writerow([filename, date, time.replace('-', ':'), dayNight, hdr['EXPTIME'], hdr['OBSERVER'], hdr['INSTRUME'], bugs, unix, temp['main']['temp'], temp['clouds']['all'], temp['visibility'], temp['weather'][0]['description']])
        except Exception as e:
            print("Error writing CSV: " + str(e))