from astropy.io import fits
import os
import datetime
dates = {}

def organize():
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
            

def getData():
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
                    if date not in dates:
                        dates[date] = {
                            "pictures": 1,
                            "telescopeUsed": file[0].header['TELESCOP'],
                            "dates": [file[0].header['DATE-OBS']]
                        }
                    else:
                        dates[date]['pictures'] += 1
                        dates[date]['dates'].append(file[0].header['DATE-OBS'])
                        if(dates[date]['telescopeUsed'] != file[0].header['TELESCOP']):
                            print('telescope mismatch')



    for date, value in dates.items():
        lowestTime = {"value": 24, "string": None}
        highestTime = {"value": 0, "string": None}
        for iso in value['dates']:
            time = iso.split('T')[1].split('-')
            hour = time[0]
            minute = time[1]
            second = time[2]
            time = int(hour) + int(minute)/60 + float(second)/3600
            print(time)
            if time > highestTime['value']:
                highestTime['string'] = f"{hour}:{minute}:{second}"
                highestTime['value'] = time
            elif time < lowestTime['value']:
                lowestTime['string'] = f"{hour}:{minute}:{second}"
                lowestTime['value'] = time
        dates[date]['lowestTime'] = lowestTime
        dates[date]['highestTime'] = highestTime
        del dates[date]['dates']

    print(dates)

getData()